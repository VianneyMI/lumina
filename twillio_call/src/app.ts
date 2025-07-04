import 'dotenv/config';
import express, { Response } from 'express';
import ExpressWs from 'express-ws';
import VoiceResponse from 'twilio/lib/twiml/VoiceResponse';
import { ElevenLabsClient } from 'elevenlabs';
import { type WebSocket } from 'ws';
import { Readable } from 'stream';

const app = ExpressWs(express()).app;
const PORT: number = parseInt(process.env.PORT || '80');

const elevenlabs = new ElevenLabsClient();
const voiceId = '21m00Tcm4TlvDq8ikWAM';
const outputFormat = 'ulaw_8000';
const text = 'This is a test. You can now hang up. Thank you.';

function startApp() {
  app.post('/call/incoming', (_, res: Response) => {
    const twiml = new VoiceResponse();

    twiml.connect().stream({
      url: `wss://${process.env.SERVER_DOMAIN}/call/connection`,
    });

    res.writeHead(200, { 'Content-Type': 'text/xml' });
    res.end(twiml.toString());
  });

  app.ws('/call/connection', (ws: WebSocket) => {
    ws.on('message', async (data: string) => {
      const message: {
        event: string;
        start?: { streamSid: string; callSid: string };
      } = JSON.parse(data);

      if (message.event === 'start' && message.start) {
        const streamSid = message.start.streamSid;
        const response = await elevenlabs.textToSpeech.convert(voiceId, {
          model_id: 'eleven_turbo_v2',
          output_format: outputFormat,
          text,
        });

        const readableStream = Readable.from(response);
        const audioArrayBuffer = await streamToArrayBuffer(readableStream);

        ws.send(
          JSON.stringify({
            streamSid,
            event: 'media',
            media: {
              payload: Buffer.from(audioArrayBuffer as any).toString('base64'),
            },
          }),
        );
      }
    });

    ws.on('error', console.error);
  });

  app.get('/', (_, res: Response) => {
    res.send(`
      <html>
        <head>
          <title>Twilio Voice Call Server</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              max-width: 800px;
              margin: 40px auto;
              padding: 20px;
              line-height: 1.6;
            }
            h1 { color: #2c3e50; }
            .info { color: #7f8c8d; }
          </style>
        </head>
        <body>
          <h1>Welcome to the Twilio Voice Call Server</h1>
          <p class="info">This server is running and ready to handle incoming calls.</p>
          <p class="info">Server is running on port: ${PORT}</p>
        </body>
      </html>
    `);
  });

  app.listen(PORT, () => {
    console.log(`Local: http://localhost:${PORT}`);
    console.log(`Remote: https://${process.env.SERVER_DOMAIN}`);
  });
}

function streamToArrayBuffer(readableStream: Readable) {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];

    readableStream.on('data', (chunk) => {
      chunks.push(chunk);
    });

    readableStream.on('end', () => {
      resolve(Buffer.concat(chunks).buffer);
    });

    readableStream.on('error', reject);
  });
}

startApp();
