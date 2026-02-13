const dataService = require("../services/dataservice");

module.exports = { executeGet };

async function executeGet({ key }) {
    if (!key) throw new Error("key required");

    return await dataService.send(`GET ${key}`);
}

module.exports = { executeGet };