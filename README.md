# Cisco Port Poller #

I created this project out of a need to monitor port information. In my case I was most interested in how many ports were setup as trunk ports and how many were up/down/shutdown, since this can be a security issue. 

The idea was to pull all of this information into a database to be used with Grafana for displaying statistics. 

## Getting Started ##
1. Using the inventory.example.yml file for reference create an inventory.yml file.
2. If using the docker-compose.yml I've included create a directory called "data", and move the inventory.yml file into it.
3. Run "docker-compose up" to build the container and run it. 

## Disclaimer ##
I'm more of a Linux/Cisco person than a programmer, but I want to commit to this project as much as possible. If anyone has suggestions or feedback of any kind please submit an issue and I'd be happy to look at it.