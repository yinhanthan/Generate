const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const pinataApiKey = '';
const pinataSecretApiKey = '';

// upload and pin an image on pinata
exports.pinFileToIPFS = async function (newYetyImage) {
    const url = 'https://api.pinata.cloud/pinning/pinFileToIPFS';

    const data = new FormData();
    data.append('file', fs.createReadStream(newYetyImage));

    return await axios
        .post(url, data, {
            maxBodyLength: 'Infinity', // Allow large file uploads
            headers: {
                'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
                pinata_api_key: pinataApiKey,
                pinata_secret_api_key: pinataSecretApiKey
            }
        });
};