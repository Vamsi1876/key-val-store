const dataService = require("../services/dataservice");

async function executeTtl({ key }) {
    if (!key) {
        throw new Error("key required");
    }
    return await dataService.send(`TTL ${key}`);
}

module.exports = { executeTtl };