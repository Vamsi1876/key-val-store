const express = require("express");
const router = express.Router();

const { executeSet } = require("../commands/set");
const { executeGet } = require("../commands/get");
const { executeDel } = require("../commands/delete");
const { executeTTL } = require("../commands/ttl");
const { executeKeys } = require("../commands/keys");
const { executeFlush } = require("../commands/flush");

router.post("/set", async (req, res) => {
    const result = await executeSet(req.body);
    res.json({ result });
});

router.get("/get/:key", async (req, res) => {
    const result = await executeGet({ key: req.params.key });
    res.json({ result });
});

router.delete("/delete/:key", async (req, res) => {
    const result = await executeDel({ key: req.params.key });
    res.json({ result });
});

router.get("/ttl/:key", async (req, res) => {
    const result = await executeTTL({ key: req.params.key });
    res.json({ result });
});

router.get("/keys", async (_, res) => {
    const result = await executeKeys();
    res.json({ result });
});

router.post("/flush", async (_, res) => {
    const result = await executeFlush();
    res.json({ result });
});

module.exports = router;
