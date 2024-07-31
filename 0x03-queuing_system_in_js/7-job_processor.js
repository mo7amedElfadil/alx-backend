#!/usr/bin/node
import { createQueue, Job } from 'kue';

const blacklist = ['4153518780', '4153518781'];
const queue = createQueue();

/**
 * sendNotification - Send a notification to a phone number
 * @param {String} phoneNumber
 * @param {String} message
 * @param {Job} job
 * @param {*} done
 */
const sendNotification = (phoneNumber, message, job, done) => {
    job.progress(0, 100);
    if (blacklist.includes(phoneNumber)) {
      return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    }
    job.progress(50, 100);
      console.log(
        `Sending notification to ${phoneNumber},`,
        `with message: ${message}`,
      );
    setTimeout(() => {
        // Complete the job successfully
        done();
    }, 1000);
};

queue.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
