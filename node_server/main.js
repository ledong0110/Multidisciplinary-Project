const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://0.tcp.ap.ngrok.io:13392'); // Replace with your MQTT broker URL

client.on('connect', function () {
  console.log('Connected to MQTT broker!');
  client.subscribe('Temp'); // Replace with the topic you want to subscribe to
});

client.on('message', function (topic, message) {
  console.log("Received message on topic ${topic}: ${message.toString()}");
  // Do whatever you want with the received message here
});