// const express = require('express');
// const app = express();
// const puppeteer = require('puppeteer');
// const { MongoClient } = require('mongodb');

// app.use(express.static('public'));

// app.get('/', (req, res) => {
//   res.sendFile(__dirname + '/index.html');
// });

// app.get('/chartData', async (req, res) => {
//   const movieName = req.query.movieName || 'Avatar_2009';
//   const userWords = req.query.userWords ? req.query.userWords.split(',') : [];

//   const browser = await puppeteer.launch();
//   let client;

//   try {
//     // Connect to MongoDB
//     const mongoDBUrl = 'mongodb+srv://imdb_adt:imdb_adt@cluster0.rcvxgzc.mongodb.net/Moviedatabase';
//     client = new MongoClient(mongoDBUrl, { useNewUrlParser: true, useUnifiedTopology: true });
//     await client.connect();

//     const database = client.db();
//     const collection = database.collection('moviedata_vectordb');

//     // Query MongoDB for all ratings and comments
//     const allRatings = await collection
//       .find({ MovieName: movieName }, { projection: { 'rating': 1, 'text': 1, 'date': 1, 'helpful': 1 } })
//       .toArray();

//     // Process ratings and generate pie chart
//     const pieChartData = processData(allRatings);

//     // Process comments and generate word cloud
//     const top20RecentComments = await collection
//       .find({ MovieName: movieName }, { projection: { 'text': 1, 'date': 1 } })
//       .sort({ 'date': -1 })
//       .limit(10)
//       .toArray();

//     const wordCloudData = generateWordCloud(top20RecentComments);

//     // Process reviews and generate bar chart data
//     const barChartData = generateBarChartData(allRatings);

//     // Process top 10 comments and helpful reviews
//     const top10Comments = generateTopComments(allRatings, 10);
//     const top10HelpfulReviews = generateTopHelpfulReviews(allRatings, 10);
//     const topCommentsMatchingWord = filterCommentsByWords(allRatings, userWords, 10);

//     // Send chart data, word cloud, and recent comments as JSON
//     res.json({
//       pieChartData,
//       wordCloudData,
//       recentComments: top20RecentComments,
//       barChartData,
//       top10Comments,
//       top10HelpfulReviews,
//       topCommentsMatchingWord,
//     });

//   } catch (error) {
//     console.error('Error:', error);
//     res.status(500).send('Internal Server Error');
//   } finally {
//     await browser.close();
//     if (client) {
//       await client.close();
//     }
//   }
// });
// // Add the following functions to filter comments by an array of words
// // Update the filterCommentsByWords function
// function filterCommentsByWords(ratings, userWords, limit) {
//   return ratings
//     .filter(movie => {
//       // Check if movie.text is defined and has a comment property
//       const commentText = movie.text?.toLowerCase();
//       return commentText && userWords.some(word => commentText.includes(word.toLowerCase()));
//     })
//     .slice(0, limit)
//     .map(movie => ({
//       date: new Date(movie.date).toLocaleDateString(),
//       comment: movie.text,
//     }));
// }

// // Update the generateTopComments function
// function generateTopComments(ratings, limit) {
//   const sortedComments = ratings
//     .filter(movie => movie.text)
//     .sort((a, b) => b.date - a.date)
//     .slice(0, limit);

//   return sortedComments.map(comment => ({
//     date: new Date(comment.date).toLocaleDateString(),
//     comment: comment.text,
//   }));
// }

// // Update the generateTopHelpfulReviews function
// function generateTopHelpfulReviews(ratings, limit) {
//   const sortedReviews = ratings
//     .filter(movie => movie.helpful !== undefined)
//     .sort((a, b) => b.helpful - a.helpful)
//     .slice(0, limit);

//   return sortedReviews.map(review => ({
//     date: new Date(review.date).toLocaleDateString(),
//     comment: review.text,
//     helpfulCount: review.helpful,
//   }));
// }

// // Update the processData function
// function processData(ratings) {
//   // Process the ratings data as needed
//   if (!Array.isArray(ratings) || ratings.length === 0) {
//     console.error('Invalid or empty ratings data');
//     return [];
//   }

//   const totalRatings = ratings.length;

//   // Process the ratings data as needed
//   const ratingCounts = {};
//   ratings.forEach((movie) => {
//     const ratingValue = movie.rating?.toString();
//     if (ratingValue) {
//       ratingCounts[ratingValue] = (ratingCounts[ratingValue] || 0) + 1;
//     }
//   });

//   // Calculate percentages with labels
//   const data = Object.entries(ratingCounts).map(([rating, count]) => ({
//     label: `${rating} - ${((count / totalRatings) * 100).toFixed(2)}%`,
//     y: count,
//   }));

//   return data;
// }

// // Update the generateWordCloud function
// function generateWordCloud(ratings) {
//   // Process the ratings data to extract comments
//   const comments = ratings.map(movie => movie.text).filter(comment => comment);

//   // Combine comments into a single string
//   const text = comments.join(' ');

//   // Implement your word cloud generation logic here
//   // You can use a JavaScript library or a service for generating word clouds

//   // For demonstration purposes, let's just return an array of words with their frequency
//   const words = text.split(/\s+/);
//   const wordCounts = {};

//   words.forEach(word => {
//     wordCounts[word] = (wordCounts[word] || 0) + 1;
//   });

//   return Object.entries(wordCounts).map(([word, count]) => ({ word, count }));
// }

// // Update the generateBarChartData function
// function generateBarChartData(ratings) {
//   // Process the ratings data to extract years and count the number of reviews in each year
//   const reviewYears = {};
//   ratings.forEach((movie) => {
//     const reviewDate = new Date(movie.date);
//     const year = reviewDate.getFullYear().toString();
//     reviewYears[year] = (reviewYears[year] || 0) + 1;
//   });

//   // Convert the data into an array format suitable for CanvasJS
//   const data = Object.entries(reviewYears).map(([year, count]) => ({
//     label: year,
//     y: count,
//   }));

//   return data;
// }
// const PORT = 3000;
// app.listen(PORT, () => {
//   console.log(`Server is running at http://localhost:${PORT}`);
// });

const express = require('express');
const app = express();
const puppeteer = require('puppeteer');
const { MongoClient } = require('mongodb');

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.get('/chartData', async (req, res) => {
  const movieName = req.query.movieName || 'Avatar_2009';
  const userWords = req.query.userWords ? req.query.userWords.split(',') : [];

  const browser = await puppeteer.launch();
  let client;

  try {
    // Connect to MongoDB
    const mongoDBUrl = 'mongodb+srv://imdb_adt:imdb_adt@cluster0.rcvxgzc.mongodb.net/Moviedatabase';
    client = new MongoClient(mongoDBUrl, { useNewUrlParser: true, useUnifiedTopology: true });
    await client.connect();

    const database = client.db();
    const collection = database.collection('moviedata_vectordb');

    // Query MongoDB for all ratings and comments
    const allRatings = await collection
      .find({ MovieName: movieName }, { projection: { 'rating': 1, 'text': 1, 'date': 1, 'helpful': 1 } })
      .toArray();

    // Process ratings and generate pie chart
    const pieChartData = processData(allRatings);

    // Process comments and generate word cloud
    const top20RecentComments = await collection
      .find({ MovieName: movieName }, { projection: { 'text': 1, 'date': 1 } })
      .sort({ 'date': -1 })
      .limit(10)
      .toArray();

    const wordCloudData = generateWordCloud(top20RecentComments);

    // Process reviews and generate bar chart data
    const barChartData = generateBarChartData(allRatings);

    // Process top 10 comments and helpful reviews
    const top10Comments = generateTopComments(allRatings, 10);
    const top10HelpfulReviews = generateTopHelpfulReviews(allRatings, 10);
    const topCommentsMatchingWord = filterCommentsByWords(allRatings, userWords, 10);

    // Send chart data, word cloud, and recent comments as JSON
    res.json({
      pieChartData,
      wordCloudData,
      recentComments: top20RecentComments,
      barChartData,
      top10Comments,
      top10HelpfulReviews,
      topCommentsMatchingWord,
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('Internal Server Error');
  } finally {
    await browser.close();
    if (client) {
      await client.close();
    }
  }
});

// Add the following functions to filter comments by an array of words
// Update the filterCommentsByWords function
function filterCommentsByWords(ratings, userWords, limit) {
  return ratings
    .filter(movie => {
      // Check if movie.text is defined and has a comment property
      const commentText = movie.text?.toLowerCase();
      return commentText && userWords.some(word => commentText.includes(word.toLowerCase()));
    })
    .slice(0, limit)
    .map(movie => ({
      date: new Date(movie.date).toLocaleDateString(),
      comment: movie.text,
    }));
}

// Update the generateTopComments function
function generateTopComments(ratings, limit) {
  const sortedComments = ratings
    .filter(movie => movie.text)
    .sort((a, b) => b.date - a.date)
    .slice(0, limit);

  return sortedComments.map(comment => ({
    date: new Date(comment.date).toLocaleDateString(),
    comment: comment.text,
  }));
}

// Update the generateTopHelpfulReviews function
function generateTopHelpfulReviews(ratings, limit) {
  const sortedReviews = ratings
    .filter(movie => movie.helpful !== undefined)
    .sort((a, b) => b.helpful - a.helpful)
    .slice(0, limit);

  return sortedReviews.map(review => ({
    date: new Date(review.date).toLocaleDateString(),
    comment: review.text,
    helpfulCount: review.helpful,
  }));
}

// Update the processData function
function processData(ratings) {
  // Process the ratings data as needed
  if (!Array.isArray(ratings) || ratings.length === 0) {
    console.error('Invalid or empty ratings data');
    return [];
  }

  const totalRatings = ratings.length;

  // Process the ratings data as needed
  const ratingCounts = {};
  ratings.forEach((movie) => {
    const ratingValue = movie.rating?.toString();
    if (ratingValue) {
      ratingCounts[ratingValue] = (ratingCounts[ratingValue] || 0) + 1;
    }
  });

  // Calculate percentages with labels
  const data = Object.entries(ratingCounts).map(([rating, count]) => ({
    label: `${rating} - ${((count / totalRatings) * 100).toFixed(2)}%`,
    y: count,
  }));

  return data;
}

// Update the generateWordCloud function
function generateWordCloud(ratings) {
  // Process the ratings data to extract comments
  const comments = ratings.map(movie => movie.text).filter(comment => comment);

  // Combine comments into a single string
  const text = comments.join(' ');

  // Implement your word cloud generation logic here
  // You can use a JavaScript library or a service for generating word clouds

  // For demonstration purposes, let's just return an array of words with their frequency
  const words = text.split(/\s+/);
  const wordCounts = {};

  words.forEach(word => {
    wordCounts[word] = (wordCounts[word] || 0) + 1;
  });

  return Object.entries(wordCounts).map(([word, count]) => ({ word, count }));
}

// Update the generateBarChartData function
function generateBarChartData(ratings) {
  // Process the ratings data to extract years and count the number of reviews in each year
  const reviewYears = {};
  ratings.forEach((movie) => {
    const reviewDate = new Date(movie.date);
    const year = reviewDate.getFullYear().toString();
    reviewYears[year] = (reviewYears[year] || 0) + 1;
  });

  // Convert the data into an array format suitable for CanvasJS
  const data = Object.entries(reviewYears).map(([year, count]) => ({
    label: year,
    y: count,
  }));

  return data;
}

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});

