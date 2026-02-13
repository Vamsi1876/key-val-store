const dataService = require("../services/dataservice");

async function executeKeys() {
    return await dataService.send("KEYS");
}

module.exports = { executeKeys };