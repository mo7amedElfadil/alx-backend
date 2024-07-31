#!/usr/bin/node
/**
 * Using Babel and ES6, write a script that connects to a Redis server
 * Logs 'Redis client connected to the server' when the connection is successful
 * Logs 'Redis client not connected to the server: ERROR_MESSAGE' when the connection is not successful
 */
import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});


/**
 * @function setNewSchool
 * @param {String} schoolName
 * @param {String} value
 * @return {undefined}
 */
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

/**
 * @function displaySchoolValue
 * @param {String} schoolName
 * @return {undefined}
 * Logs the value of the schoolName key
 */
function displaySchoolValue(schoolName) {
  client.get(schoolName, (_, value) => {
    console.log(value);
  });
}


displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
