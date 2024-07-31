#!/usr/bin/node
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const app = express();

const client = createClient({ name: 'reserve_seat' });
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const queue = createQueue();

let reservationEnabled = true;

const port = 1245;

/**
 * @function reserveSeat - Modifies the number of available seats.
 * @param {number} number - The new number of seats.
 * @returns {Promise<String>}
 */
async function reserveSeat(number) {
  return setAsync('available_seats', number);
};

/**
 * @function getCurrentAvailableSeats - Retrieves the number of available seats.
 * @returns {Promise<String>}
 */
async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return parseInt(availableSeats, 10);
};

/**
 * initialize the number of available seats
 */
(async () => {
  await reserveSeat(50);
})();

app.get('/available_seats', (_, res) => {
  getCurrentAvailableSeats()
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats })
    });
});

app.get('/reserve_seat', (_req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  const job = queue.create('reserve_seat')
    .on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', (err) => {
      console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
    })
    .save((err) => {
      if (err) {
        res.json({ status: 'Reservation failed' });
      }
    }
    );
  res.json({ status: 'Reservation in process' });
});

app.get('/process', (_, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', (_, done) => {
    getCurrentAvailableSeats()
      .then((result) => {
        return parseInt(result, 10);
      })
      .then((availableSeats) => {
        reservationEnabled = availableSeats <= 1 ? false : reservationEnabled;
        if (availableSeats >= 1) {
            reserveSeat(availableSeats - 1)
            .then(() => done());
        } else {
          done(new Error('Not enough seats available'));
        }
      });
  });
});

const resetAvailableSeats = async (initialSeatsCount) => {
  return setAsync('available_seats', Number.parseInt(initialSeatsCount));
};

app.listen(port, () => {
  resetAvailableSeats(50)
    .then(() => {
      reservationEnabled = true;
      console.log(`API available on localhost port ${port}`);
    });
});

export default app;
