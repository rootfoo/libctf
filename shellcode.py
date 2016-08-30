import ctypes
import pkgutil
import json
from capstone import *
from data import splitevery
import struct
import socket

JSON_FILE = 'shellcode.json'
factory = None


def iptoint(ip):
    """convert IPv4 address to integer"""
    return int(socket.inet_aton(ip).encode('hex'),16)


def inttoip(ip):
    """convert integer to IPv4 address"""
    return socket.inet_ntoa(hex(ip)[2:].decode('hex'))


def disassemble(shellcode, offsets=True, opcodes=True, dissas=True):
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    address = 0x00
    instructions = cs.disasm(shellcode, address)
    ins_list = []
    justify_width = 16
    for insn in instructions:
        offset = "{0:08x}:".format(insn.address) if offsets else ""
        bytestr = ' '.join(splitevery(str(insn.bytes).encode('hex'), 2)).ljust(justify_width) if opcodes else ""
        bytestr += " :" if bytestr else ""
        asm = "{0} {1}".format(insn.mnemonic, insn.op_str) if dissas else ""
        print "{0} {1} {2}".format(offset, bytestr, asm)
        ins_list.append(insn)
    return ins_list
    


class ShellcodeFactory(object):

    def __init__(self, json_path=None):
        self._path = json_path
        self._json = None

        # load json data from file
        if json_path: 
            with open(json_path) as fh:
                self._json = json.load(fh)

        # try to load json data from installation directory
        elif __package__:
            data = pkgutil.get_data(__package__, JSON_FILE)
            self._json = json.loads(data)

        else:
            raise(Exception("JSON file could not be found"))

   
    def get(self, key, **kwargs):
        j = None
        
        # get shellcode by index
        if type(key) == int:
            j = self._json[key]
        
        # get shellcode from list by name
        else:
            j = filter(lambda d: d['name']==key, self._json)[0]
            
        # set params
        if 'params' in j:
            for k,d in j['params'].iteritems():
                if k in kwargs:
                    d['value'] = kwargs[k]

                elif 'default' in d:
                    d['value'] = d['default']

                else:
                    raise(Exception("error setting parameter value for " + k))

        # return shellcode 
        return Shellcode(j)


    
    def show(self, key=None):
        if not key is None:
            sc = self.get(key)
            sc.show()
        
        else:
            i = 0
            for sc in self._json:
                print "{index}: {name} - {quick}".format(index=i, name=sc['name'], quick=sc['quick'])
                i += 1




def shellcode(name, **kwargs):
    """convenience function to find and return shellcode by name"""
    global factory 
    if not factory:
        factory = ShellcodeFactory()
    return factory.get(name, **kwargs) 



class Shellcode(object):

    def __init__(self, json):
        self.__dict__ = json
        self.raw = self.shellcode.decode('base64')
       
        # apply parameters if specified
        if hasattr(self, 'params'):
            for name,vdict in self.params.iteritems():
                value = vdict['value']
                offset = vdict['offset']

                # pack according to parameter type
                if name.lower() == 'ipv4':
                    self.set(offset, iptoint(value), '>I')
                
                elif name.lower() == 'port':
                    self.set(offset, value, '<H')

 
    def set(self, offset, value, pack_fmt=None):
        """overwrite shellcode value at offset. struct.pack(value, fmt) first if format specified"""
        # pack if specified
        value = struct.pack(pack_fmt, value) if pack_fmt else value
        self.raw = self.raw[:offset] + value + self.raw[offset+len(value):]
        # update shellcode attribute to reflect changes
        self.shellcode = self.raw.encode('base64')


    def show(self):
        for k,v in self.__dict__.iteritems():
            if not (k.startswith('_') or k in ['raw', 'params']):
                print "{} : {}".format(k,v).strip()

        if hasattr(self, 'params'):
            params = []
            for k,vd in self.params.iteritems():
                params.append("{k} ({d})".format(k=k, d=vd['value']))
            print "params: ", ', '.join(params)

    
    def __str__(self):
        return self.raw


    def disas(self, offsets=True, opcodes=True, dissas=True):
        disassemble(self.raw, offsets, opcodes, dissas)


