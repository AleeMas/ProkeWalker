import constant
import pymem


class MemoryOperation:
    processMemory = pymem.Pymem("PROClient.exe")

    # Read from process memory given the process memory (arg0),
    # the module name (arg1), the starting offset (arg2) and the offsets (arg3)
    @staticmethod
    def read_from_memory(module_name, starting_offset, offsets):
        module = pymem.process.module_from_name(MemoryOperation.processMemory.process_handle, module_name)
        base_address = module.lpBaseOfDll
        pointer_static_address = base_address + starting_offset
        address = MemoryOperation.follow_address(offsets, pointer_static_address)
        value = MemoryOperation.processMemory.read_int(address)
        return value

    # Follow pointers in memory given the process memory (arg0), the offsets (arg1) and the starting pointer (arg2)
    @staticmethod
    def follow_address(offsets, pointer_static_address):
        for offset in offsets:
            pointer_static_address = MemoryOperation.processMemory.read_longlong(pointer_static_address)
            pointer_static_address = pointer_static_address + offset
        return pointer_static_address

    @staticmethod
    def get_pokemon_id():
        return MemoryOperation.read_from_memory(constant.MODULE_GAME_ASSEMBLY, constant.POKE_ID_OFFSET, constant.POKE_ID)
