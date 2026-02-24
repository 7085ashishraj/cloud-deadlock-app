import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = `http://${window.location.hostname}:8000/api`;

function App() {
  const [processId, setProcessId] = useState('');
  const [resourceId, setResourceId] = useState('');
  const [reqProcess, setReqProcess] = useState('');
  const [reqResource, setReqResource] = useState('');
  const [allocProcess, setAllocProcess] = useState('');
  const [allocResource, setAllocResource] = useState('');
  const [message, setMessage] = useState('');
  const [deadlockResult, setDeadlockResult] = useState(null);
  const [graphUrl, setGraphUrl] = useState(null);

  const handleAction = async (endpoint, payload, successMsg) => {
    try {
      await axios.post(`${API_BASE}/${endpoint}`, payload);
      setMessage(`Success: ${successMsg}`);
      setDeadlockResult(null); // Clear previous results on new action
      setGraphUrl(null);
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleDetect = async () => {
    try {
      const response = await axios.get(`${API_BASE}/detect`);
      setDeadlockResult(response.data);
      setMessage("Detection complete.");
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  const handleVisualize = async () => {
    try {
      setMessage("Generating graph upload...");
      const response = await axios.get(`${API_BASE}/visualize`);
      setGraphUrl(response.data.url);
      setMessage("Graph visualization generated!");
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  const handleReset = async () => {
    try {
      await axios.post(`${API_BASE}/reset`);
      setMessage("System reset successfully.");
      setDeadlockResult(null);
      setGraphUrl(null);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans p-6 selection:bg-cyan-500/30">

      {/* Header */}
      <header className="max-w-5xl mx-auto flex flex-col items-center justify-center mb-12 mt-8 text-center space-y-4">
        <h1 className="text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500 tracking-tight">
          Cloud Deadlock Detector
        </h1>
        <p className="text-slate-400 text-lg md:text-xl max-w-2xl">
          Visualize and detect process-resource interactions dynamically in the cloud.
        </p>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">

        {/* Node Creation Cards */}
        <section className="space-y-8">
          {/* Add Process */}
          <div className="bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 p-6 rounded-2xl shadow-xl hover:shadow-cyan-500/10 transition-all duration-300">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="bg-cyan-500/20 text-cyan-400 p-2 rounded-lg text-sm "><svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg></span>
              Register Process
            </h2>
            <div className="flex gap-3">
              <input
                type="text"
                placeholder="e.g. P1"
                value={processId}
                onChange={e => setProcessId(e.target.value)}
                className="flex-1 bg-slate-900/50 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all text-white placeholder-slate-500"
              />
              <button
                onClick={() => handleAction('process', { id: processId }, `Process ${processId} added`)}
                className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold px-6 py-3 rounded-xl transition-colors shadow-lg shadow-cyan-500/20"
              >
                Add
              </button>
            </div>
          </div>

          {/* Add Resource */}
          <div className="bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 p-6 rounded-2xl shadow-xl hover:shadow-blue-500/10 transition-all duration-300">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="bg-blue-500/20 text-blue-400 p-2 rounded-lg text-sm "><svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"></path></svg></span>
              Register Resource
            </h2>
            <div className="flex gap-3">
              <input
                type="text"
                placeholder="e.g. R1"
                value={resourceId}
                onChange={e => setResourceId(e.target.value)}
                className="flex-1 bg-slate-900/50 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-white placeholder-slate-500"
              />
              <button
                onClick={() => handleAction('resource', { id: resourceId }, `Resource ${resourceId} added`)}
                className="bg-blue-500 hover:bg-blue-400 text-slate-900 font-semibold px-6 py-3 rounded-xl transition-colors shadow-lg shadow-blue-500/20"
              >
                Add
              </button>
            </div>
          </div>
        </section>

        {/* Edge Creation Cards */}
        <section className="space-y-8">
          {/* Request Resource */}
          <div className="bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 p-6 rounded-2xl shadow-xl hover:shadow-purple-500/10 transition-all duration-300">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="bg-purple-500/20 text-purple-400 p-2 rounded-lg text-sm ">↗</span>
              Process Requests Resource
            </h2>
            <div className="flex gap-3 items-center">
              <input type="text" placeholder="Process ID" value={reqProcess} onChange={e => setReqProcess(e.target.value)} className="w-1/3 bg-slate-900/50 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all" />
              <span className="text-slate-500 font-bold">→</span>
              <input type="text" placeholder="Resource ID" value={reqResource} onChange={e => setReqResource(e.target.value)} className="w-1/3 bg-slate-900/50 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all" />
              <button onClick={() => handleAction('request', { process_id: reqProcess, resource_id: reqResource }, `Process ${reqProcess} requested Resource ${reqResource}`)} className="flex-1 bg-purple-500 hover:bg-purple-400 text-slate-900 font-semibold py-3 rounded-xl transition-colors shadow-lg shadow-purple-500/20">Submit</button>
            </div>
          </div>

          {/* Allocate Resource */}
          <div className="bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 p-6 rounded-2xl shadow-xl hover:shadow-emerald-500/10 transition-all duration-300">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="bg-emerald-500/20 text-emerald-400 p-2 rounded-lg text-sm ">↙</span>
              Resource Allocated to Process
            </h2>
            <div className="flex gap-3 items-center">
              <input type="text" placeholder="Resource ID" value={allocResource} onChange={e => setAllocResource(e.target.value)} className="w-1/3 bg-slate-900/50 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all" />
              <span className="text-slate-500 font-bold">→</span>
              <input type="text" placeholder="Process ID" value={allocProcess} onChange={e => setAllocProcess(e.target.value)} className="w-1/3 bg-slate-900/50 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all" />
              <button onClick={() => handleAction('allocate', { process_id: allocProcess, resource_id: allocResource }, `Resource ${allocResource} allocated to ${allocProcess}`)} className="flex-1 bg-emerald-500 hover:bg-emerald-400 text-slate-900 font-semibold py-3 rounded-xl transition-colors shadow-lg shadow-emerald-500/20">Submit</button>
            </div>
          </div>
        </section>
      </main>

      {/* Actions and Status */}
      <div className="max-w-3xl mx-auto mt-12 flex flex-col items-center space-y-8">
        {message && (
          <div className="bg-slate-800/80 backdrop-blur py-3 px-6 rounded-full border border-slate-700/50 text-slate-300 animate-fade-in">
            {message}
          </div>
        )}

        <div className="flex flex-wrap gap-4 w-full justify-center">
          <button
            onClick={handleDetect}
            className="group relative px-8 py-4 bg-gradient-to-r from-red-500 to-rose-600 text-white font-bold rounded-2xl shadow-xl shadow-red-500/20 hover:shadow-red-500/40 hover:-translate-y-1 transition-all duration-300 overflow-hidden"
          >
            <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
            <span className="relative flex items-center gap-3">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              Run Detection
            </span>
          </button>

          <button
            onClick={handleVisualize}
            className="group relative px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-600 text-white font-bold rounded-2xl shadow-xl shadow-blue-500/20 hover:shadow-blue-500/40 hover:-translate-y-1 transition-all duration-300 overflow-hidden"
          >
            <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
            <span className="relative flex items-center gap-3">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
              View Cloud Graph
            </span>
          </button>

          <button
            onClick={handleReset}
            className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-2xl shadow-xl border border-slate-700/50 transition-all duration-300"
          >
            Reset System
          </button>
        </div>

        {/* Visualization Panel */}
        {graphUrl && (
          <div className="w-full mt-8 flex flex-col items-center animate-fade-in text-center p-6 border border-cyan-500/30 bg-cyan-900/10 rounded-2xl">
            <h3 className="text-2xl font-bold text-cyan-400 mb-6 flex items-center gap-2"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg> Resource Allocation Graph</h3>
            <img src={`${API_BASE.replace('/api', '')}${graphUrl}?t=${new Date().getTime()}`} alt="Deadlock Graph" className="rounded-xl border border-slate-700 shadow-2xl shadow-cyan-500/10 max-w-full h-auto bg-white/90 p-2" />
            <p className="text-slate-500 mt-4 text-xs font-mono break-all bg-black/50 p-2 rounded">🔗 URL: {graphUrl}</p>
          </div>
        )}

        {/* Results Panel */}
        {deadlockResult && (
          <div className={`w-full p-8 rounded-3xl border ${deadlockResult.has_deadlock ? 'bg-red-900/20 border-red-500/50 backdrop-blur-md' : 'bg-emerald-900/20 border-emerald-500/50 backdrop-blur-md'} animate-fade-in shadow-2xl`}>
            <h3 className={`text-3xl font-bold mb-4 flex items-center gap-3 ${deadlockResult.has_deadlock ? 'text-red-400' : 'text-emerald-400'}`}>
              {deadlockResult.has_deadlock ? '🚨 Deadlock Detected!' : '✅ System is Safe'}
            </h3>

            {deadlockResult.has_deadlock && (
              <div className="mt-6 space-y-4">
                <p className="text-slate-300 text-lg">The following circular wait(s) were found:</p>
                <div className="grid gap-3">
                  {deadlockResult.cycles.map((cycle, idx) => (
                    <div key={idx} className="bg-slate-900/50 border border-red-500/30 p-4 rounded-xl font-mono text-red-300 flex items-center gap-3 overflow-x-auto">
                      <span className="bg-red-500/20 px-3 py-1 rounded text-sm text-red-400 font-bold">Cycle {idx + 1}</span>
                      {cycle.join(' ➔ ')} ➔ {cycle[0]}
                    </div>
                  ))}
                </div>
              </div>
            )}
            {!deadlockResult.has_deadlock && (
              <p className="text-slate-300 text-lg">No cycles detected in the resource allocation graph.</p>
            )}
          </div>
        )}
      </div>

    </div>
  );
}

export default App;
