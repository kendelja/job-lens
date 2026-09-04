import { useEffect, useState } from "react";

function Dashboard() {
    const [jobs, setJobs] = useState([]);

    const [search, setSearch] = useState("");
    const [remoteFilter, setRemoteFilter] = useState("all");
    const [sourceFilter, setSourceFilter] = useState("all");

    useEffect(() => {
        fetch("http://localhost:8000/jobs/")
            .then((response) => response.json())
            .then((data) => setJobs(data))
            .catch((error) => {
                console.error("Failed to fetch jobs:", error);
            });
    }, []);

    const filteredJobs = jobs.filter((job) => {
        const searchText = search.toLowerCase();

        const matchesSearch =
            job.title?.toLowerCase().includes(searchText) ||
            job.company?.toLowerCase().includes(searchText);

        const matchesRemote =
            remoteFilter === "all" ||
            job.remote_type?.toLowerCase() === remoteFilter;

        const matchesSource =
            sourceFilter === "all" ||
            job.source?.toLowerCase() === sourceFilter;

        return matchesSearch && matchesRemote && matchesSource;
    });

    return (
        <div className="app">

            <header className="topbar">
                <div>
                    <div className="logo">JobLens</div>
                    <p>Find better jobs, faster.</p>
                </div>

                <div className="job-count">
                    {filteredJobs.length} jobs
                </div>
            </header>


            <main className="dashboard">

                <section className="hero">
                    {/* <h1>Discover your next opportunity.</h1> */}

                    <p>
                        Search jobs from multiple sources in one place.
                    </p>
                </section>


                <section className="filters">

                    <div className="search-wrapper">
                        <span>⌕</span>

                        <input
                            type="text"
                            placeholder="Search jobs or companies..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>

                    <select
                        value={remoteFilter}
                        onChange={(e) => setRemoteFilter(e.target.value)}
                    >
                        <option value="all">
                            All locations
                        </option>

                        <option value="remote">
                            Remote
                        </option>

                        <option value="remote only">
                            Remote only
                        </option>

                        <option value="on-site">
                            On-site
                        </option>
                    </select>

                    <select
                        value={sourceFilter}
                        onChange={(e) => setSourceFilter(e.target.value)}
                    >
                        <option value="all">
                            All sources
                        </option>

                        <option value="builtin">
                            Built In
                        </option>

                        <option value="wellfound">
                            Wellfound
                        </option>
                    </select>

                </section>


                <div className="results-header">
                    <span>
                        {filteredJobs.length} matching jobs
                    </span>
                </div>


                <section className="job-list">

                    {filteredJobs.map((job) => (

                        <article
                            className="job-card"
                            key={job.id}
                        >

                            <div className="company-logo">

                                {job.company_logo ? (
                                    <img
                                        src={job.company_logo}
                                        alt={`${job.company} logo`}
                                    />
                                ) : (
                                    <span>
                                        {job.company?.charAt(0)}
                                    </span>
                                )}

                            </div>


                            <div className="job-content">

                                <div className="job-main">

                                    <h2>{job.title}</h2>

                                    <div className="company">
                                        {job.company}
                                    </div>

                                    <div className="job-meta">

                                        {job.location && (
                                            <span>
                                                📍 {job.location}
                                            </span>
                                        )}

                                        {job.remote_type && (
                                            <span className="tag remote">
                                                {job.remote_type}
                                            </span>
                                        )}

                                    </div>

                                </div>


                                <div className="job-right">

                                    {job.salary_min && (
                                        <div className="salary">

                                            ${Math.round(
                                                job.salary_min / 1000
                                            )}k

                                            {job.salary_max &&
                                                ` – $${Math.round(
                                                    job.salary_max / 1000
                                                )}k`
                                            }

                                        </div>
                                    )}

                                    <span className="source">
                                        {job.source}
                                    </span>

                                </div>

                            </div>


                            <a
                                className="view-job"
                                href={job.url}
                                target="_blank"
                                rel="noreferrer"
                            >
                                →
                            </a>

                        </article>

                    ))}

                </section>

            </main>

        </div>
    );
}


export default Dashboard;