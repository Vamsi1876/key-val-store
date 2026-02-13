const dataService = require("../services/dataservice");

async function executeFlush() {
    return await dataService.send("FLUSH");
}

module.exports = { executeFlush };