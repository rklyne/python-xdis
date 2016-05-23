"""
CPython 2.4 bytecode opcodes

This is used in bytecode disassembly.

This is used in bytecode disassembly. This is equivalent of to the
opcodes in Python's opcode.py library.
"""

from copy import deepcopy

import pyxdis.opcodes.opcode_2x as opcode_2x

# FIXME: can we DRY this even more?

# Make a *copy* of opcode_2x values so we don't pollute 2x
hasconst = list(opcode_2x.hasconst)
hascompare = list(opcode_2x.hascompare)
hasfree = list(opcode_2x.hasfree)
haslocal = list(opcode_2x.haslocal)
hasnargs = list(opcode_2x.hasnargs)
opmap = list(opcode_2x.opmap)
opname = list(opcode_2x.opname)
EXTENDED_ARG = opcode_2x.EXTENDED_ARG

for object in opcode_2x.fields2copy:
    globals()[object] =  deepcopy(getattr(opcode_2x, object))

def updateGlobal():
    globals().update(dict([(k.replace('+', '_'), v) for (k, v) in opcode_2x.opmap.items()]))
    globals().update({'JUMP_OPs': map(lambda op: opcode_2x.opname[op],
                                          opcode_2x.hasjrel + opcode_2x.hasjabs)})
    return

# Can't use opcode 2_x since we want to update *our* opname and opmap
def def_op(name, op):
    opname[op] = name
    opmap[name] = op

# Bytecodes added since 2.3
def_op('NOP', 9)
def_op('LIST_APPEND', 18)
def_op('YIELD_VALUE', 86)

updateGlobal()

# Remove def_op no importers are tempted to use it.
del def_op

from pyxdis import PYTHON_VERSION
if PYTHON_VERSION == 2.4:
    import dis
    # print(set(dis.opmap.items()) - set(opmap.items()))
    # print(set(opmap.items()) - set(dis.opmap.items()))
    assert all(item in opmap.items() for item in dis.opmap.items())
    assert all(item in dis.opmap.items() for item in opmap.items())
