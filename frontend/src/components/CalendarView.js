// frontend/src/components/CalendarView.js
import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import JobModal from './JobModal';
import CreateJobModal from './CreateJobModal';
import Button from 'react-bootstrap/Button';

const localizer = momentLocalizer(moment);

const CalendarView = () => {
    const [jobs, setJobs] = useState([]);
    const [selectedJob, setSelectedJob] = useState(null);
    const [teamMembers, setTeamMembers] = useState([]);
    const [indexes, setIndexes] = useState([]);
    const [viewType, setViewType] = useState('month');
    const [modalOpen, setModalOpen] = useState(false);
    const [createModalOpen, setCreateModalOpen] = useState(false);
    const [selectedDate, setSelectedDate] = useState(null);

    // Fetch jobs, team members, and indexes on component mount
    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [jobsResponse, membersResponse, indexesResponse] = await Promise.all([
                axios.get('http://localhost:8000/api/jobs/'),
                axios.get('http://localhost:8000/api/team-members/'),
                axios.get('http://localhost:8000/api/indexes/')
            ]);

            // Format job data for the calendar
            const formattedJobs = jobsResponse.data.map(job => ({
                id: job.id,
                title: job.title,
                start: new Date(job.start_time),
                end: new Date(job.end_time),
                index: job.index,
                index_name: job.index_name,
                assigned_to: job.assigned_to,
                assigned_to_name: job.assigned_to_name,
                color: job.color,
                notes: job.notes,
            }));

            setJobs(formattedJobs);
            setTeamMembers(membersResponse.data);
            setIndexes(indexesResponse.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    // Handle event click (job selection)
    const handleSelectEvent = (event) => {
        setSelectedJob(event);
        setModalOpen(true);
    };

    // Handle slot selection (for creating new jobs)
    const handleSelectSlot = (slotInfo) => {
        setSelectedDate(slotInfo.start);
        setCreateModalOpen(true);
    };

    // Handle job assignment update
    const handleAssignJob = async (jobId, teamMemberId) => {
        try {
            const response = await axios.put(`http://localhost:8000/api/assign-job/${jobId}/`, {
                team_member_id: teamMemberId
            });

            // Update the jobs state with the updated job
            setJobs(prevJobs =>
                prevJobs.map(job =>
                    job.id === jobId
                        ? {
                            ...job,
                            assigned_to: response.data.assigned_to,
                            assigned_to_name: response.data.assigned_to_name
                        }
                        : job
                )
            );

            // Close the modal
            setModalOpen(false);
        } catch (error) {
            console.error('Error assigning job:', error);
        }
    };

    // Handle new job creation
    const handleJobCreated = (newJob) => {
        const formattedJob = {
            id: newJob.id,
            title: newJob.title,
            start: new Date(newJob.start_time),
            end: new Date(newJob.end_time),
            index: newJob.index,
            index_name: newJob.index_name,
            assigned_to: newJob.assigned_to,
            assigned_to_name: newJob.assigned_to_name,
            color: newJob.color,
            notes: newJob.notes,
        };

        setJobs([...jobs, formattedJob]);
    };

    // Custom event styling
    const eventStyleGetter = (event) => {
        const style = {
            backgroundColor: event.color || '#3174ad',
            borderRadius: '4px',
            opacity: 0.8,
            color: 'white',
            border: '0px',
            display: 'block',
            fontWeight: 'bold'
        };
        return {
            style
        };
    };

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h2>Job Schedule Calendar</h2>
                <div className="d-flex gap-2">
                    <Button variant="success" onClick={() => setCreateModalOpen(true)}>
                        Add New Job
                    </Button>
                    <div className="btn-group">
                        <button
                            className={`btn ${viewType === 'month' ? 'btn-primary' : 'btn-outline-primary'}`}
                            onClick={() => setViewType('month')}
                        >
                            Month
                        </button>
                        <button
                            className={`btn ${viewType === 'week' ? 'btn-primary' : 'btn-outline-primary'}`}
                            onClick={() => setViewType('week')}
                        >
                            Week
                        </button>
                        <button
                            className={`btn ${viewType === 'day' ? 'btn-primary' : 'btn-outline-primary'}`}
                            onClick={() => setViewType('day')}
                        >
                            Day
                        </button>
                    </div>
                </div>
            </div>

            <div style={{ height: 800 }}>
                <Calendar
                    localizer={localizer}
                    events={jobs}
                    startAccessor="start"
                    endAccessor="end"
                    style={{ height: '100%' }}
                    eventPropGetter={eventStyleGetter}
                    onSelectEvent={handleSelectEvent}
                    onSelectSlot={handleSelectSlot}
                    selectable={true}
                    view={viewType}
                    onView={setViewType}
                    views={['month', 'week', 'day']}
                />
            </div>

            {modalOpen && (
                <JobModal
                    job={selectedJob}
                    teamMembers={teamMembers}
                    onAssign={handleAssignJob}
                    onClose={() => setModalOpen(false)}
                />
            )}

            {createModalOpen && (
                <CreateJobModal
                    indexes={indexes}
                    teamMembers={teamMembers}
                    selectedDate={selectedDate}
                    onClose={() => {
                        setCreateModalOpen(false);
                        setSelectedDate(null);
                    }}
                    onJobCreated={handleJobCreated}
                />
            )}
        </div>
    );
};

export default CalendarView;