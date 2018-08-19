#include <iostream>
#include "RakPeer.h"

int main() {
    
    RakNet::RakPeerInterface *server = RakNet::RakPeerInterface::GetInstance();
    RakNet::SocketDescriptor socketDescriptor(0,0);
    if (server->Startup(2, &socketDescriptor, 1) == RakNet::RAKNET_STARTED)
        printf("RakServer started\n");
    RakNet::RakPeerInterface::DestroyInstance(server);
    return 0;
}
