#include <cstdlib>
#include <iostream>
#include <boost/bind.hpp>
#include <boost/asio.hpp>

#include "icmp_header.hpp"
#include "ipv4_header.hpp"

using boost::asio::ip::icmp;

class Server
{
public:
	Server(boost::asio::io_service& io_service)
			: io_service_(io_service),  socket_(io_service, icmp::endpoint(icmp::v4(), 0))
	{
		socket_.async_receive_from(
				reply_buffer_.prepare(max_length), sender_endpoint_,
				boost::bind(&Server::handle_receive_from, this,
						boost::asio::placeholders::error,
						boost::asio::placeholders::bytes_transferred));
	}


	void handle_receive_from(const boost::system::error_code& error,
			size_t bytes_recvd)
	{
		if (!error && bytes_recvd > 0)
		{
			reply_buffer_.commit(bytes_recvd);
			std::istream is(&reply_buffer_);
			ipv4_header ipv4_hdr;
			icmp_header icmp_hdr;
			std::vector<unsigned char> mask = {255, 255, 0, 0};

			is >> ipv4_hdr >> icmp_hdr;
			if (is && icmp_hdr.type() == icmp_header::address_request) {
				icmp_hdr.type(icmp_header::address_reply);
				icmp_hdr.code(0);
				boost::asio::streambuf request_buffer;
				std::ostream os(&request_buffer);
				compute_checksum(icmp_hdr, mask.begin(), mask.end());
				os << icmp_hdr <<  mask[0] << mask[1] << mask[2] << mask[3];

				socket_.async_send_to(
						request_buffer.data(), sender_endpoint_,
						boost::bind(&Server::handle_send_to, this,
								boost::asio::placeholders::error,
								boost::asio::placeholders::bytes_transferred));
			} else {
				reply_buffer_.consume(reply_buffer_.size());
				socket_.async_receive_from(
						reply_buffer_.prepare(max_length), sender_endpoint_,
						boost::bind(&Server::handle_receive_from, this,
								boost::asio::placeholders::error,
								boost::asio::placeholders::bytes_transferred));
			}
		} else {
			reply_buffer_.consume(reply_buffer_.size());
			socket_.async_receive_from(
					reply_buffer_.prepare(max_length), sender_endpoint_,
					boost::bind(&Server::handle_receive_from, this,
							boost::asio::placeholders::error,
							boost::asio::placeholders::bytes_transferred));
		}
	}

	void handle_send_to(const boost::system::error_code& error, size_t size)
	{
		reply_buffer_.consume(reply_buffer_.size());
		socket_.async_receive_from(
				reply_buffer_.prepare(max_length), sender_endpoint_,
				boost::bind(&Server::handle_receive_from, this,
						boost::asio::placeholders::error,
						boost::asio::placeholders::bytes_transferred));
	}

private:
	boost::asio::io_service& io_service_;
	icmp::socket socket_;
	icmp::endpoint sender_endpoint_;
	const int max_length = 65536;
	boost::asio::streambuf reply_buffer_;
};

int main(int argc, char* argv[])
{
	boost::asio::io_service io_service;
	Server s(io_service);
	io_service.run();

	return 0;
}
