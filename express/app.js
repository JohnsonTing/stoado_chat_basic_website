// backend/index.js
const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');


const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

app.post('/classify', async (req, res) => {
  const { number } = req.body;
  try {
    const response = await axios.post('http://localhost:5001/classify', { number });
    console.log(response.data.result)
    res.json({ result: response.data.result });
  } catch (error) {
    console.error(error);
    res.status(500).send('Error classifying number');
  }
});

app.all('*', (req, res) => {
  res.status(404).send('<h1>resource not found</h1>')
})

app.listen(PORT, () => {
  console.log(`Server is running on port 5000`);
});
