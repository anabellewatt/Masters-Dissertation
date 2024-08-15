const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000; // Use environment variable for port or default to 3000

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Route to serve the consent page
app.get('/consent.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'consent.html'));
});

// Route to serve the survey page
app.get('/Survey.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'Survey.html'));
});



// Route to handle form submission from the consent page
app.post('/submit-consent', (req, res) => {
    const { agreed } = req.body;

    if (agreed === true) {
        res.redirect('/Survey.html'); // Redirect to the survey page if agreed
    } else {
        res.status(400).send('Consent not given'); // Handle if consent is not given
    }
});

// Route to handle form submission from the survey page
app.post('/end.html', (req, res) => {
    const surveyData = req.body
    const filename = `survey-${Date.now()}.json`;
    const filePath = path.join(__dirname, 'data', filename);

    fs.writeFile(filePath, JSON.stringify(surveyData, null, 2), (err) => {
        if (err) {
            console.error('Error saving survey:', err);
            res.status(500).send('Error saving survey');
        } else {
            // Send a success response
            res.status(200).send('Survey saved successfully');

            // Optionally, you can also log a message to indicate the file path
            console.log('Survey data saved to:', filePath);
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
