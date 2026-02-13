const dataService = require("../services/dataservice");

async function executeDelete({ key }) {
    if (!key) {
        throw new Error("key required");
    }
    return await dataService.send(`DEL ${key}`);
}

module.exports = { executeDelete };