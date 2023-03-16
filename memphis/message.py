from __future__ import annotations

import json

from memphis.exceptions import MemphisConnectError


class Message:
    def __init__(self, message, connection, cg_name):
        self.message = message
        self.connection = connection
        self.cg_name = cg_name

    async def ack(self):
        """Ack a message is done processing."""
        try:
            await self.message.ack()
        except Exception as e:
            if (
                "$memphis_pm_id" in self.message.headers
                and "$memphis_pm_sequence" in self.message.headers
            ):
                try:
                    msg = {
                        "id": self.message.headers["$memphis_pm_id"],
                        "sequence": self.message.headers["$memphis_pm_sequence"],
                    }
                    msgToAck = json.dumps(msg).encode("utf-8")
                    await self.connection.broker_manager.publish(
                        "$memphis_pm_acks", msgToAck
                    )
                except Exception as er:
                    raise MemphisConnectError(str(er)) from er
            else:
                raise MemphisConnectError(str(e)) from e
            return

    def get_data(self):
        """Receive the message."""
        try:
            return bytearray(self.message.data)
        except:
            return

    def get_headers(self):
        """Receive the headers."""
        try:
            return self.message.headers
        except:
            return

    def get_sequence_number(self):
        """Get message sequence number."""
        try:
            return self.message.metadata.sequence.stream
        except:
            return
