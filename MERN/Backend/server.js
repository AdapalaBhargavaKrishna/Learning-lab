const express = require("express");
const app = express();

const PORT = 5000;

app.use(express.json());

let videos = [
  { id: 1, title: "Node js", duration: "11min" },
  { id: 2, title: "React js", duration: "10min" },
  { id: 3, title: "Express js", duration: "7min" },
  { id: 4, title: "Next js", duration: "20min" },
];

app.get("/", (req, res) => {
  res.send("Hello World!");
});

// CREATE

app.post("/videos", (req, res, next) => {
  const video = req.body;

  if (!video || !video.title || !video.duration) {
    const err = new Error("Invalid Video Data.");
    err.statusCode = 400;
    return next(err);
  }

  const newId = videos.length ? videos[videos.length - 1].id + 1 : 1;

  videos.push({ id: newId, ...video });
  res.json({ message: "Video added", video: { id: newId, ...video } });
});

// READ

app.get("/videos", (req, res, next) => {
  if (!videos.length) {
    const err = new Error("No video found.");
    err.statusCode = 404;
    return next(err);
  }
  res.json(videos);
});

app.get("/videos/:id", (req, res, next) => {
  const videoId = parseInt(req.params.id);

  const video = videos.find((v) => v.id === videoId);
  if (video) {
    res.json(video);
  } else {
    const err = new Error("No video found.");
    err.statusCode = 404;
    return next(err);
  }
});

// UPDATE

app.put("/videos/:id", (req, res, next) => {
  const videoId = parseInt(req.params.id);
  const updatedVideo = req.body;

  const video = videos.find((v) => v.id === videoId);

  if (video) {
    if (!updatedVideo.title && !updatedVideo.duration) {
      const err = new Error("Nothing to update.");
      err.statusCode = 400;
      return next(err);
    }
    video.title = updatedVideo.title || video.title;
    video.duration = updatedVideo.duration || video.duration;
    res.json({ message: "Video updated", video });
  } else {
    const err = new Error("No video found.");
    err.statusCode = 404;
    return next(err);
  }
});

// DELETE

app.delete("/videos/:id", (req, res, next) => {
  const videoId = parseInt(req.params.id);
  let video = videos.find((v) => v.id === videoId);

  if (!video) {
    const err = new Error("No video found.");
    err.statusCode = 404;
    return next(err);
  }

  videos = videos.filter((v) => v.id !== videoId);
  res.json({ message: "Video deleted", id: videoId, video });
});

app.use((err, req, res, next) => {
  console.log(err.stack);

  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    success: false,
    message: err.message || "Something went wrong!",
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
