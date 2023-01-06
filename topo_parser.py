from mininet.topo import Topo


def extract_info(string):
    # Split the string into a list of substrings at each space character
    parts = string.split()
    # Gets the input
    input_num = parts[0][1:2]
    # Gets the Type
    type = parts[1][1]
    # Gets the dst
    connectTo = parts[1][3:19]
    # Gets the dst_input
    connectToInput = parts[1][21:22]

    # Return a tuple with the extracted information
    return input_num, type, connectTo, connectToInput


class FatTreeTopo(Topo):
    def __init__(self):
        super(FatTreeTopo, self).__init__()
        self.mapName = dict()
        self.count = 0
        self.to_print = {}

    def parse_topology_file(self, filepath):
        # Open the file for reading
        with open(filepath, 'r') as f:
            for line in f:
                s = line.split()
                if line == '':
                    pass
                else:
                    if str.startswith(line, 'sysimgguid='):
                        words = line.split('=')
                        sysimg_guid = words[1]
                        line = next(f).strip()
                    if str.startswith(line, 'switchguid='):
                        words = line.split('=')
                        switch_guid = words[1]
                    else:
                        if str.startswith(line, 'Switch') or str.startswith(line, 'Ca'):
                            # When reaching a Switch connection , define a new Node if doesnt Exist yet
                            # and connect all his connections
                            words = s
                            type_of_cur_mechine = words[0]
                            if type_of_cur_mechine == "Switch" or type_of_cur_mechine == 'Ca':
                                switch_name = (words[2].split('-')[1]).split('"')[0]
                                if type_of_cur_mechine == "Switch":
                                    # switch_name = switch_name.encode('ascii')
                                    self.addSwitch(switch_name)
                                else:
                                    self.addHost(switch_name)
                                self.mapName[switch_name] = sysimg_guid
                                con = True
                                while con:
                                    try:
                                        # throw exception when reach to the end
                                        line = next(f)
                                        # if got an empty line
                                        if len(line) == 1:
                                            con = False
                                        else:
                                            # Split the line into words and save the data as followed:
                                            # inputnum : the index that need to be connected
                                            # connectto : the name of the node that need to be connected
                                            # atinput : the index of node connectto
                                            info = extract_info(line)
                                            inputnum = info[0]
                                            typo_mechine = info[1]
                                            connectto = info[2]
                                            atinput = info[3]
                                            if typo_mechine == 'S':
                                                self.addSwitch(connectto)
                                            else:
                                                self.addHost(connectto)
                                            atinputInt = (int(atinput))
                                            inputnumInt = (int(inputnum))
                                            self.addLink(switch_name, connectto, inputnumInt, atinputInt)
                                            self.addConnection(type_of_cur_mechine, typo_mechine, switch_name,
                                                               connectto, inputnum, atinput)
                                    except:
                                        return self

    def addConnection(self, type_of_cur_mechine1, typo_mechine2, switch_name1, connectto2, inputnum1, atinput2):
        # Parse the print message by the switch and hosts types

        if typo_mechine2 == 'S':
            typo_mechine2 = 'Switch'
        else:
            typo_mechine2 = 'Host'
        if type_of_cur_mechine1 == 'Ca':
            type_of_cur_mechine1 = 'Host'
        tup = type_of_cur_mechine1 + ':' + '\n' + "sysimgguid=" + self.mapName[
            switch_name1] + "Port_id=" + switch_name1 + ', Conncted to ' + typo_mechine2 + ": switchguid=" + connectto2 + " , port=(" + inputnum1 + ")" + '\n'
        inputnum1 = int(inputnum1)
        atinput2 = int(atinput2)
        # self.setlinkInfo( inputnum1, atinput2 , tup , switch_name1)
        self.to_print[self.count] = tup
        self.count = self.count + 1

    def print_connections(self):
        # order of connectivity keeps here , and print them by their order
        for tup in self.to_print:
            print(self.to_print[tup])


M = FatTreeTopo()

M = FatTreeTopo.parse_topology_file(M, '../topoFolder/TopologyFiles/small_topo_file')
# M = FatTreeTopo.parse_topology_file(M, '../topoFolder/TopologyFiles/large_topo_file')

FatTreeTopo.print_connections(M)
