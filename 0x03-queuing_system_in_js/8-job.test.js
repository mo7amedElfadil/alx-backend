#!/usr/bin/node
import { createQueue } from 'kue';
import { expect } from 'chai';
import sinon from 'sinon';
import createPushNotificationsJobs from './8-job.js';


/**
 * @function testPushNotifications
 * test suite for createPushNotificationsJobs
 * uses queue.testMode to test the jobs to validate which jobs are inside the queue
 * @return {undefined}
 */

function testPushNotifications() {
  describe('createPushNotificationsJobs', function () {
    const queue = createQueue({ name: 'push_notification_test' });
    let consoleSpy;
    const jobData = [
      { phoneNumber: '1234567890', message: 'message1' },
      { phoneNumber: '1234567890', message: 'message2' },
      { phoneNumber: '1234567890', message: 'message3' },
    ];

    beforeEach(() => {
      queue.testMode.enter();
      consoleSpy = sinon.spy(console, 'log');
    });

    afterEach(() => {
      queue.testMode.clear();
      consoleSpy.restore();
      consoleSpy.resetHistory();
    });

    before(() => {
      queue.testMode.enter();
    });

    after(() => {
      queue.testMode.clear();
      queue.testMode.exit();
    });

    it('throws an error if jobs is not an array', function () {
      expect(() => createPushNotificationsJobs('jobData', queue)).to.throw('Jobs is not an array');
    });

    it('does not throw an error if jobs is an array', function () {
      expect(() => createPushNotificationsJobs(jobData, queue)).to.not.throw();
    });

    it('creates jobs in the queue', function () {
      createPushNotificationsJobs(jobData, queue);
      expect(queue.testMode.jobs.length).to.equal(3);
      expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
      expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
      expect(queue.testMode.jobs[2].type).to.equal('push_notification_code_3');
    });


    it('adding jobs to the queue', function () {
      expect(queue.testMode.jobs.length).to.equal(0);
      createPushNotificationsJobs(jobData, queue);
      for (let i = 0; i < jobData.length; i++) {
        expect(queue.testMode.jobs[i].data).to.deep.equal(jobData[i]);
      }
      queue.process('push_notification_test', () => {
      expect(
        consoleSpy
        .calledWith('Notification job created:', queue.testMode.jobs[0].id)
      ).to.be.true;
    }
      );
    });


    it('checks that jobs have appropriate listeners', function () {
      createPushNotificationsJobs(jobData, queue);
      const job = queue.testMode.jobs[0];
      expect(job).to.have.property('_events');
      expect(job._events).to.have.property('enqueue');
      expect(job._events).to.have.property('complete');
      expect(job._events).to.have.property('failed');
      expect(job._events).to.have.property('progress');
    });

  });
}

testPushNotifications();
