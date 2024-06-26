# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import jimon_pb2 as jimon__pb2


class JimonStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UpdateAndAck = channel.unary_unary(
                '/jimon.Jimon/UpdateAndAck',
                request_serializer=jimon__pb2.MsgUpdate.SerializeToString,
                response_deserializer=jimon__pb2.MsgAck.FromString,
                )


class JimonServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UpdateAndAck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JimonServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UpdateAndAck': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateAndAck,
                    request_deserializer=jimon__pb2.MsgUpdate.FromString,
                    response_serializer=jimon__pb2.MsgAck.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'jimon.Jimon', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Jimon(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UpdateAndAck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jimon.Jimon/UpdateAndAck',
            jimon__pb2.MsgUpdate.SerializeToString,
            jimon__pb2.MsgAck.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
