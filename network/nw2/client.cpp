#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <istream>
#include <iostream>
#include <ostream>

#include "icmp_header.hpp"
#include "ipv4_header.hpp"

using boost::asio::ip::icmp;
using boost::asio::deadline_timer;
namespace posix_time = boost::posix_time;

class Client
{
public:
	Client(boost::asio::io_service& io_service, const char* destination)
			:socket_(io_service, icmp::v4()), timer_(io_service),
 			sequence_number_(0), is_ok(false)
	{
		icmp::resolver::query query(icmp::v4(), destination, "");
		icmp::resolver resolver_(io_service);
		destination_ = *resolver_.resolve(query);
		start_send();
	}

private:
	void start_send()
	{
		std::vector<unsigned char> ip = {0, 0, 0, 0};
		icmp_header address_request;
		address_request.type(icmp_header::address_request);
		address_request.code(0);
		address_request.identifier(get_identifier());
		address_request.sequence_number(++sequence_number_);
		compute_checksum(address_request, ip.begin(), ip.end());

		boost::asio::streambuf request_buffer;
		std::ostream os(&request_buffer);
		os << address_request << ip[0] << ip[1] << ip[2] << ip[3];
		socket_.send_to(request_buffer.data(), destination_);
		timer_.expires_at(posix_time::microsec_clock::universal_time() +
				posix_time::seconds(5));
		timer_.async_wait(boost::bind(&Client::handle_timeout, this));
		start_receive();
	}

	void handle_timeout()
	{
		if (!is_ok) {
			std::cout << "Request timed out." << std::endl;
		}
		timer_.expires_at(posix_time::microsec_clock::universal_time() + posix_time::seconds(2));
    timer_.async_wait(boost::bind(&Client::start_send, this));
	}

	void start_receive()
	{
		reply_buffer_.consume(reply_buffer_.size());
		socket_.async_receive(reply_buffer_.prepare(65536),
				boost::bind(&Client::handle_receive, this, _2));
	}

	void handle_receive(std::size_t length)
	{
		reply_buffer_.commit(length);
		std::istream is(&reply_buffer_);
		ipv4_header ipv4_hdr;
		icmp_header icmp_hdr;
		unsigned char mask[4];

		is >> ipv4_hdr >> icmp_hdr >> mask[0] >> mask[1] >> mask[2] >> mask[3];
		if (is && icmp_hdr.type() == icmp_header::address_reply
				&& icmp_hdr.identifier() == get_identifier()
				&& icmp_hdr.sequence_number() == sequence_number_)
		{
			timer_.cancel();
			is_ok = true;
			std::cout << "Mask: " << (int)mask[0] << "." << (int)mask[1] <<"."
					<< (int)mask[2] << "." <<(int)mask[3] << std::endl;
		}
		
		start_receive();
	}

	static unsigned short get_identifier()
	{
		return static_cast<unsigned short>(::getpid());
	}

	icmp::endpoint destination_;
	icmp::socket socket_;
	deadline_timer timer_;
	unsigned short sequence_number_;
	boost::asio::streambuf reply_buffer_;
	bool is_ok;
};

int main(int argc, char* argv[])
{
	if (argc != 2)
	{
		std::cerr << "Usage: client <host>" << std::endl;
		return 1;
	}
	boost::asio::io_service io_service;
	Client p(io_service, argv[1]);
	io_service.run();

	return 0;
}
