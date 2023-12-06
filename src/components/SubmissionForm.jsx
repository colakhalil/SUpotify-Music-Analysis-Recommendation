import React, { useState } from 'react';
import "../pagesCSS/SubmissionForm.css";
const SubmissionForm = () => {
  const [fileData, setFileData] = useState(null);
  const [showWarning, setShowWarning] = useState(false);
  const [formData, setFormData] = useState({
    songTitle: '',
    artistName: '',
    songGenre: '',
    songMood: '',
    songDuration: '',
    songReleaseYear: '',
  });

  const isFormComplete = () => {
    return formData.songTitle && formData.artistName && formData.songGenre 
           && formData.songMood && formData.songDuration && formData.songReleaseYear;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          // Perform validation on data here
          if (isValidData(data)) {
            setFileData(data);
          } else {
            console.error('Invalid file format');
          }
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      };
      reader.readAsText(file);
    } else {
      console.error('Please upload a valid JSON file');
    }
  };
  const handleImportSubmit = async () => {
    if (fileData) {
      // Send fileData to the backend
      try {
        const response = await fetch('/your-api-endpoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(fileData)
        });
        // Handle response...
      } catch (error) {
        console.error('Error:', error);
      }
    } else {
      console.error('No valid data to submit');
    }
  };
  const isValidData = (data) => {
    // Define the expected fields in order
    const expectedFields = ['songTitle', 'artistName', 'songGenre','songMood', 'songDuration', 'songReleaseYear' ];
  
    // Check if all required fields are present and in order
    return expectedFields.every((field, index) => {
      return Object.keys(data)[index] === field && data.hasOwnProperty(field);
    });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isFormComplete()) {
      setShowWarning(true); // Show warning pop-up
      return; // Prevent further execution
    }
    setShowWarning(false);
    try {
      const response = await fetch('/your-api-endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        console.log('Song data submitted successfully');
        // Handle successful submission, e.g., clearing the form or giving user feedback
      } else {
        console.error('Failed to submit song data');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form className="submission-form" onSubmit={handleSubmit}>
      <h2>Add a song to the database</h2>
      <p>Please provide the details of the song you want to add</p>
      <input
        type="text"
        name="songTitle"
        value={formData.songTitle}
        onChange={handleChange}
        placeholder="Song Title"
      />
      <input
        type="text"
        name="artistName"
        value={formData.artistName}
        onChange={handleChange}
        placeholder="Artist's Name"
      />
      <input
        type="text"
        name="songGenre"
        value={formData.songGenre}
        onChange={handleChange}
        placeholder="Song's Genre"
      />
        <input
        type="text"
        name="songMood"
        value={formData.songMood}
        onChange={handleChange}
        placeholder="Song's Mood"
      />
      
      <input
        type="text"
        name="songDuration"
        value={formData.songDuration}
        onChange={handleChange}
        placeholder="Song's Duration in seconds"
      />
      <input
        type="text"
        name="songReleaseYear"
        value={formData.songReleaseYear}
        onChange={handleChange}
        placeholder="Song's Release Year"
      />
      <button type="submit" disabled={!isFormComplete()}>Submit</button>
      {showWarning  && (
        <div className="warning-popup">
          Please fill out all fields before submitting.
        </div>
      )}
      <input type= "file" accept='.json' onChange={handleFileChange}/>
      <button type='submit' onClick={handleImportSubmit}>Import</button>


      
    </form>
  );
};

export default SubmissionForm;
