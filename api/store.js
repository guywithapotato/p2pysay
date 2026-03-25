let messages = [];

export function addMessage(sender, text) {
  messages.push({ sender, text, time: Date.now() });
  if (messages.length > 100) messages = messages.slice(-100);
}

export function getMessages() {
  return messages;
}
