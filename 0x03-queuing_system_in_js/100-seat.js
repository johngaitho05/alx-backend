import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const PORT = 1245;

const client = redis.createClient();
const queue = kue.createQueue();

const reserveSeat = (number) => {
  return promisify(client.set).bind(client)('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const getAsync = promisify(client.get).bind(client);
  const availableSeats = await getAsync('available_seats');
  return parseInt(availableSeats) || 0;
};

app.use(express.json());

let reservationEnabled = true;

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });
  const currentAvailableSeats = await getCurrentAvailableSeats();
  if (currentAvailableSeats <= 0) {
    reservationEnabled = false;
    return;
  }
  const newAvailableSeats = currentAvailableSeats - 1;
  await reserveSeat(newAvailableSeats);
  if (newAvailableSeats === 0) {
    reservationEnabled = false;
  }
});

queue.process('reserve_seat', async (job, done) => {
  try {
    await getCurrentAvailableSeats();
    const currentAvailableSeats = await getCurrentAvailableSeats();
    if (currentAvailableSeats <= 0) {
      done(new Error('Not enough seats available'));
      return;
    }
    console.log(`Seat reservation job ${job.id} completed`);
    done();
  } catch (error) {
    done(error);
  }
});


app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});

reserveSeat(50);
