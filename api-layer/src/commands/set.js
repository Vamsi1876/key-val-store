const dataService = require("../services/dataservice");

async function executeSet({ key, value, ttl }) {
    if (!key || !value) {
        throw new Error("key and value required");
    }

    let cmd = `SET ${key} "${value}"`;

    if (ttl) {
        cmd += ` EX ${ttl}`;
    }

    return await dataService.send(cmd);
}

module.exports = { executeSet };