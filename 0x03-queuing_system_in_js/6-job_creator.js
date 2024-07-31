#!/usr/bin/node
/**
 * Create a queue using Kue
 */
import { createQueue } from 'kue';

const queue = createQueue();

const jobData = {
  phonenumber: '123345465',
  message: 'test message',
};

const job = queue.create('push_notification_code', jobData)
  .on('complete', () => {
  console.log('Notification job completed');
})
  .on('failed', () => {
  console.log('Notification job failed');
})
  .save((err) => {
  if (!err) console.log(`Notification job created: ${job.id}`);
});



