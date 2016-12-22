from enum import Enum
from libbitcoin.bc.config import ffi, lib
from libbitcoin.bc.data import DataChunk, DataStack
from libbitcoin.bc.error import ErrorCode
from libbitcoin.bc.hash import HashDigest
from libbitcoin.bc.operation import Operation, OperationList
from libbitcoin.bc.string import String

class Script:

    def __init__(self, obj=None):
        if obj is None:
            obj = lib.bc_create_script()
        self._obj = obj

    def __del__(self):
        lib.bc_destroy_script(self._obj)

    @classmethod
    def from_ops(cls, ops):
        obj = lib.bc_create_script_Ops(ops._obj)
        return cls(obj)

    @classmethod
    def from_data(cls, encoded, prefix):
        data = DataChunk(encoded)
        obj = lib.bc_create_script_Data(data._obj, prefix)
        return cls(obj)

    def copy(self):
        obj = lib.bc_create_script_copy(self._obj)
        return Script(obj)

    def __eq__(self, other):
        return lib.bc_script__equals(self._obj, other._obj) == 1

    def from_string(self, mnemonic):
        if isinstance(mnemonic, str):
            mnemonic = bytes(mnemonic, "ascii")
        return lib.bc_script__from_string(self._obj, mnemonic) == 1

    def is_valid(self):
        return lib.bc_script__is_valid(self._obj) == 1

    def is_valid_operations(self):
        return lib.bc_script__is_valid_operations(self._obj) == 1

    def to_data(self, prefix):
        obj = lib.bc_script__to_data(self._obj, prefix)
        return DataChunk(obj).data

    def to_string(self, active_forks):
        obj = lib.bc_script__to_string(self._obj, active_forks)
        return str(String(obj))

    def empty(self):
        return lib.bc_script__empty(self._obj) == 1

    def size(self):
        return lib.bc_script__size(self._obj)

    def front(self):
        obj = lib.bc_script__front(self._obj)
        return Operation(obj)

    def back(self):
        obj = lib.bc_script__back(self._obj)
        return Operation(obj)

    def at(self, index):
        obj = lib.bc_script__at(self._obj, index)
        return Operation(obj)

    def satoshi_content_size(self):
        return lib.bc_script__satoshi_content_size(self._obj)

    def serialized_size(self, prefix):
        return lib.bc_script__serialized_size(self._obj)

    def operations(self):
        obj = lib.bc_script__operations(self._obj)
        return OperationList(obj)

    @staticmethod
    def generate_signature_hash(tx, input_index,
                                script_code, sighash_type):
        obj = lib.bc_script__generate_signature_hash(
            tx._obj, input_index, script_code._obj, sighash_type.value)
        return HashDigest(obj)

    @staticmethod
    def check_signature(signature, sighash_type, public_key,
                        script_code, tx, input_index):
        public_key = DataChunk(public_key)
        return lib.bc_script__check_signature(
            signature._obj, sighash_type.value, public_key._obj,
            script_code._obj, tx._obj, input_index) == 1

    @staticmethod
    def create_endorsement(out, secret, prevout_script, tx,
                           input_index, sighash_type):
        return lib.bc_script__create_endorsement(
            out._obj, secret._obj, prevout_script._obj, tx._obj,
            input_index, sighash_type.value) == 1

    def is_enabled(self, active_forks, fork):
        """Determine if the fork is enabled in the active forks set."""
        return lib.bc_script__is_enabled(self._obj, active_forks,
                                         fork.value) == 1

    def is_push_only(self, ops):
        return lib.bc_script__is_push_only(self._obj, ops._obj) == 1

    def is_relaxed_push(self, ops):
        return lib.bc_script__is_relaxed_push(self._obj, ops._obj) == 1

    def is_coinbase_pattern(self, ops, height):
        return lib.bc_script__is_coinbase_pattern(self._obj, ops._obj,
                                                  height) == 1

    def is_null_data_pattern(self, ops):
        return lib.bc_script__is_null_data_pattern(self._obj, ops._obj) == 1

    def is_pay_multisig_pattern(self, ops):
        return lib.bc_script__is_pay_multisig_pattern(self._obj, ops._obj) == 1

    def is_pay_public_key_pattern(self, ops):
        return lib.bc_script__is_pay_public_key_pattern(self._obj,
                                                        ops._obj) == 1

    def is_pay_key_hash_pattern(self, ops):
        return lib.bc_script__is_pay_key_hash_pattern(self._obj, ops._obj) == 1

    def is_pay_script_hash_pattern(self, ops):
        return lib.bc_script__is_pay_script_hash_pattern(self._obj,
                                                         ops._obj) == 1

    def is_sign_multisig_pattern(self, ops):
        return lib.bc_script__is_sign_multisig_pattern(self._obj, ops._obj) == 1

    def is_sign_public_key_pattern(self, ops):
        return lib.bc_script__is_sign_public_key_pattern(self._obj,
                                                         ops._obj) == 1

    def is_sign_key_hash_pattern(self, ops):
        return lib.bc_script__is_sign_key_hash_pattern(self._obj, ops._obj) == 1

    def is_sign_script_hash_pattern(self, ops):
        return lib.bc_script__is_sign_script_hash_pattern(self._obj,
                                                          ops._obj) == 1

    @staticmethod
    def to_null_data_pattern(data):
        data = DataChunk(data)
        obj = lib.bc_script__to_null_data_pattern(data._obj)
        return OperationList(obj)

    @staticmethod
    def to_pay_public_key_pattern(data):
        data = DataChunk(data)
        obj = lib.bc_script__to_pay_public_key_pattern(data._obj)
        return OperationList(obj)

    @staticmethod
    def to_pay_key_hash_pattern(hash):
        obj = lib.bc_script__to_pay_key_hash_pattern(hash._obj)
        return OperationList(obj)

    @staticmethod
    def to_pay_script_hash_pattern(hash):
        obj = lib.bc_script__to_pay_script_hash_pattern(hash._obj)
        return OperationList(obj)

    @staticmethod
    def to_pay_multisig_pattern(signatures, points):
        if isinstance(points, list):
            return Script._to_pay_multisig_pattern_DataStack(signatures, points)
        # Not yet implemented
        return None

    @staticmethod
    def _to_pay_multisig_pattern_DataStack(signatures, points):
        raise Exception
        for point in points:
            pass

    def sigops(self, embedded):
        return lib.bc_script__sigops(self._obj, embedded)

    def embedded_sigops(self, prevout_script):
        return lib.bc_script__embedded_sigops(self._obj, prevout_script._obj)

    def find_and_delete(self, endorsements):
        stack = DataStack()
        for endorse in endorsements:
            endorse = DataChunk(endorse)
            stack.append(endorse)
        lib.bc_script__find_and_delete(self._obj, stack._obj)

    @staticmethod
    def verify(tx, input, forks):
        obj = lib.bc_script__verify(tx._obj, input, forks)
        return ErrorCode(obj)

