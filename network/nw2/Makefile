all: client server
	
	
client:
	g++ client.cpp icmp_header.hpp ipv4_header.hpp -lboost_system -std=c++11 -o client

server:
	g++ server.cpp icmp_header.hpp ipv4_header.hpp -std=c++11 -lboost_system -o server
	
clean:
	rm client server
