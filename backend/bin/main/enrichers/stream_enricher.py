import hashlib

from main.helpers.print_helper import PrintHelper


class StreamEntry:
    def __init__(self, combined_string, stream_id):
        self.combined_string = combined_string
        self.stream_id = stream_id

class StreamEnricher:
    def __init__(self):
        self.stream_ids = {"": ""}
        self.header = "traffic_analyzer_tcp_stream"

    def print(self):
        print_text = "Print out for {} tcp stream entries"
        PrintHelper.print_dict(self.stream_ids, print_text)

    def get_stream_id(self, packet):
        inbound_outbound_string = self.get_combined_strings(packet)
        if inbound_outbound_string in self.stream_ids:
            return self.stream_ids[inbound_outbound_string]

        stream_entry = self.generate_stream_id(inbound_outbound_string)
        self.set_entry(stream_entry)
        return stream_entry.stream_id

    @staticmethod
    def get_combined_strings(packet):
        dst_ip = packet["ip.dst"]
        src_ip = packet["ip.src"]
        tcp_dst_port = packet["tcp.dstport"]
        tcp_src_port = packet["tcp.srcport"]
        udp_dst_port = packet["udp.dstport"]
        udp_src_port = packet["udp.srcport"]

        if (tcp_dst_port is "" and tcp_src_port is "") and (udp_dst_port is "" and udp_src_port is ""):
            return ""

        timestamp = packet["frame.time"]
        inbound = ",".join([dst_ip, src_ip, tcp_dst_port, tcp_src_port, udp_dst_port, udp_src_port])
        outbound = ",".join([src_ip, dst_ip, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port])
        inbound_outbound_list = [inbound, outbound]
        inbound_outbound_list.sort()

        return ";".join(inbound_outbound_list)

    @staticmethod
    def generate_stream_id(combined_string):
        hash_value = hashlib.sha256(combined_string.encode())
        stream_id = int(hash_value.hexdigest(), 16) % 100000000
        return StreamEntry(combined_string, stream_id)

    def set_entry(self, stream_entry):
        self.stream_ids[stream_entry.combined_string] = stream_entry.stream_id