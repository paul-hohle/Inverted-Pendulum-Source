//*****************************************************************************************

#include <iostream>
#include <sstream>
#include <cassert>

//*****************************************************************************************

#include <array>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <forward_list>
#include <string>

//*****************************************************************************************

#include "net.hpp"

//*****************************************************************************************

#include <msgpack.hpp>
#include <nngpp/nngpp.h>

#include <nngpp/protocol/req0.h>
#include <nngpp/protocol/rep0.h>


//*****************************************************************************************

int nng_test() try {
	// create a socket for the rep protocol
	nng::socket rep_sock = nng::rep::open();
	
	// rep starts listening using the tcp transport
	rep_sock.listen( "tcp://localhost:6666" );
	
	// create a socket for the req protocol
	nng::socket req_sock = nng::req::open();
	
	// req dials and establishes a connection
	req_sock.dial( "tcp://localhost:6666" );
	
	// req sends "hello" including the null terminator
	req_sock.send("hello");
	
	// rep receives a message
	nng::buffer rep_buf = rep_sock.recv();
	
	// check the content
	if( rep_buf == "hello" ) {
		// rep sends "world" in response
		rep_sock.send("world");
               std::cout << "Send world in response" << std::endl;
	}
	
	// req receives "world"
	nng::buffer req_buf = req_sock.recv();

        return(0);
}

//----------------------------------------------------------------------------------

catch( const nng::exception& e ) {
	// who() is the name of the nng function that produced the error
	// what() is a description of the error code
	printf( "%s: %s\n", e.who(), e.what() );
	return 1;
}
// req_buf is freed
// rep_buf is freed
// req_sock is closed
// rep_sock is closed


//*****************************************************************************************

void packet()

{
    std::tuple<int , double, double, double, double> t(0x2000,1.0, 2.0, 3.0,4.0);
    std::stringstream ss;
    msgpack::pack(ss, t);

    auto const& str = ss.str();
    auto oh         = msgpack::unpack(str.data(), str.size());
    auto obj        = oh.get();

    std::cout << obj << std::endl;

    assert(obj.as<decltype(t)>() == t);
}



