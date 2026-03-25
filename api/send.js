import { addMessage, getMessages } from './store.js';

export default function handler(req, res) {
  if (req.method === 'POST') {
    const { sender, text } = req.body;
    addMessage(sender, text);
    res.status(200).json({ ok: true });
  } else {
    res.status(200).json(getMessages());
  }
}
