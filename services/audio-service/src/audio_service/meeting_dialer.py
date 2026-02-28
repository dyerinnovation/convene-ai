"""Meeting dialer using Twilio to place outbound calls."""

from __future__ import annotations

import logging

from twilio.rest import Client as TwilioClient

logger = logging.getLogger(__name__)


class MeetingDialer:
    """Initiates outbound calls via Twilio to join meetings.

    Uses TwiML to:
    1. Pause briefly for the call to connect.
    2. Send DTMF tones to enter the meeting code.
    3. Start a bidirectional Media Stream for audio processing.

    Attributes:
        _client: Authenticated Twilio REST client.
        _from_number: The Twilio phone number to call from.
    """

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        from_number: str,
    ) -> None:
        """Initialise the dialer with Twilio credentials.

        Args:
            account_sid: Twilio account SID.
            auth_token: Twilio auth token.
            from_number: The Twilio phone number (E.164 format).
        """
        self._client = TwilioClient(account_sid, auth_token)
        self._from_number = from_number

    def _build_twiml(
        self,
        meeting_code: str,
        stream_url: str,
    ) -> str:
        """Build TwiML for dialling into a meeting.

        The generated TwiML:
        - Pauses 2 seconds for the IVR to start.
        - Sends DTMF digits for the meeting code followed by ``#``.
        - Opens a bidirectional Media Stream WebSocket.

        Args:
            meeting_code: The meeting access code to enter via DTMF.
            stream_url: WebSocket URL for the Media Stream endpoint.

        Returns:
            A TwiML XML string.
        """
        # 'w' in <Play> digits adds a 0.5s pause; use 4 for ~2s wait
        dtmf_digits = f"wwww{meeting_code}#"
        return (
            "<Response>"
            f'  <Play digits="{dtmf_digits}"/>'
            "  <Connect>"
            f'    <Stream url="{stream_url}" />'
            "  </Connect>"
            "</Response>"
        )

    async def dial(
        self,
        dial_in_number: str,
        meeting_code: str,
        stream_url: str,
    ) -> str:
        """Place an outbound call and join a meeting.

        Creates a Twilio outbound call with TwiML that enters the
        meeting code via DTMF and opens a Media Stream for
        bidirectional audio.

        Args:
            dial_in_number: The meeting dial-in phone number (E.164).
            meeting_code: The meeting access code.
            stream_url: WebSocket URL for the audio stream endpoint.

        Returns:
            The Twilio Call SID for the initiated call.
        """
        twiml = self._build_twiml(meeting_code, stream_url)

        logger.info(
            "Dialing meeting: number=%s, code=%s",
            dial_in_number,
            meeting_code,
        )

        call = self._client.calls.create(
            to=dial_in_number,
            from_=self._from_number,
            twiml=twiml,
        )

        logger.info("Call initiated: sid=%s", call.sid)
        return str(call.sid)
