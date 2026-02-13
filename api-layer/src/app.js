const express = require("express");
const app = express();

app.use(express.json());

const kvRoutes = require("./routes/kvRoutes");
app.use("/kv", kvRoutes);

app.listen(3000, () => {
    console.log("API running on port 3000");
});
