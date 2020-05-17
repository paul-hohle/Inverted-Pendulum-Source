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

#include <msgpack.hpp>
#include <nngpp/nngpp.h>

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

//*****************************************************************************************

int main(void)

{
    packet();
}
