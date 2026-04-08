import React, { useState } from 'react';
import { Brain, Dna, Activity, Server, ShieldCheck, CheckCircle } from 'lucide-react';

function App() {
  const [mriFile, setMriFile] = useState(null);
  const [dnaFile, setDnaFile] = useState(null);
  const [inferenceData, setInferenceData] = useState(null);
  const [swarmPlan, setSwarmPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  const runFullPipeline = async () => {
    if (!mriFile || !dnaFile) {
      alert("Please select both MRI and Genomic files first.");
      return;
    }
    
    setLoading(true);
    try {
      // 1. Prepare the files for secure cloud transport
      const formData = new FormData();
      formData.append("mri", mriFile);
      formData.append("dna", dnaFile);

      // 2. Send actual files to the FastAPI Backend
      const response = await fetch('https://crispy-train-q7q6g4v569g6fxgjx-8000.app.github.dev/api/inference', {
        method: 'POST',
        body: formData, 
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // 3. Update the UI with the dynamic, multi-modal results
      setInferenceData({
        vision_output: data.vision_output,
        genomic_output: data.genomic_output
      });
      setSwarmPlan(data.full_plan);

    } catch (error) {
      console.error("Pipeline Error:", error);
      alert("System Error: Check if FastAPI backend is running, Port 8000 is Public, and URL is correct.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen w-full bg-slate-950 text-slate-200 p-4 md:p-10">
      <header className="max-w-6xl mx-auto mb-10 border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-black text-emerald-400 flex items-center gap-3 tracking-tighter">
          <Activity size={32} /> MEDICA-EMPOWER-PRO
        </h1>
        <p className="text-slate-500 uppercase text-xs tracking-widest mt-1">Autonomous Diagnostic Swarm // v2.0 Enterprise</p>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Left Column: Data Ingestion */}
        <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-2xl backdrop-blur-sm">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><Server size={20} className="text-blue-500" /> DEEP LEARNING INGESTION</h2>
          
          <div className="space-y-6">
            {/* MRI Upload Box */}
            <label className="block p-6 border-2 border-dashed border-slate-800 rounded-xl hover:border-blue-500/50 transition-colors cursor-pointer group">
              <input type="file" className="hidden" onChange={(e) => setMriFile(e.target.files[0])} />
              <div className="flex items-center gap-4">
                <Brain className={mriFile ? "text-emerald-400" : "text-slate-600"} size={40} />
                <div>
                  <p className="font-bold">{mriFile ? mriFile.name : "Upload 3D MRI (.nii.gz)"}</p>
                  <p className="text-xs text-slate-500 uppercase">Swin-UNETR Transformer Input</p>
                </div>
                {mriFile && <CheckCircle size={20} className="ml-auto text-emerald-400" />}
              </div>
            </label>

            {/* DNA Upload Box */}
            <label className="block p-6 border-2 border-dashed border-slate-800 rounded-xl hover:border-emerald-500/50 transition-colors cursor-pointer group">
              <input 
                type="file" 
                className="hidden" 
                onChange={(e) => setDnaFile(e.target.files[0])} 
              />
              <div className="flex items-center gap-4">
                <Dna className={dnaFile ? "text-emerald-400" : "text-slate-600"} size={40} />
                <div>
                  <p className="font-bold">{dnaFile ? dnaFile.name : "Upload Genomic Data (.fasta)"}</p>
                  <p className="text-xs text-slate-500 uppercase tracking-widest">GNN Interaction Mapping</p>
                </div>
                {dnaFile && <CheckCircle size={20} className="ml-auto text-emerald-400" />}
              </div>
            </label>

            <button 
              onClick={runFullPipeline}
              disabled={loading}
              className="w-full py-4 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white font-black rounded-xl transition-all shadow-lg shadow-blue-900/20"
            >
              {loading ? "PROCESSING TENSORS..." : "INITIALIZE NEURAL ENGINES"}
            </button>
          </div>
        </div>

        {/* Right Column: Swarm Logic */}
        <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-2xl flex flex-col">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><ShieldCheck size={20} className="text-emerald-500" /> SWARM CONSENSUS</h2>
          
          <div className="flex-grow flex flex-col justify-center">
            {!inferenceData ? (
              <div className="text-center p-10 border border-slate-800 rounded-xl bg-slate-950/50 italic text-slate-600">
                System Awaiting Perception Input...
              </div>
            ) : (
              <div className="space-y-6">
                <div className="p-4 bg-black rounded-lg border border-slate-800 font-mono text-xs text-emerald-500">
                   {inferenceData.vision_output}<br/><br/>{inferenceData.genomic_output}
                </div>
                <div className="p-6 bg-slate-950 border-l-4 border-emerald-500 rounded-r-lg shadow-lg">
                  <p className="text-sm leading-relaxed text-slate-300 whitespace-pre-line">{swarmPlan}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;