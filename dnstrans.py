import dns.zone
import dns.resolver
import argparse


parser = argparse.ArgumentParser(description='Enter domain to parse and attempt a DNS Zone Transfer')
parser.add_argument("domain")
args = parser.parse_args()
print('Domain entered: ' + args.domain)

my_resolver = dns.resolver.Resolver()

ns_servers = []
def dns_zone_xfer(address):
    ns_answer = my_resolver.resolve(address, 'NS')
    for server in ns_answer:
        print("[] Found NS: {}".format(server))
        ip_answer = my_resolver.resolve(server.target, 'A')
        for ip in ip_answer:
            print("[] IP for {} is {}".format(server, ip))
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(str(ip), address))
                for host in zone:
                    print("[] Found Host: {}".format(host))
            except Exception as e:
                print("[] NS {} REFUSED ZONE TRANSFER!".format(server))
                continue

dns_zone_xfer(args.domain)
