import React, { useState, useEffect } from 'react';
import { Copy, Check, Sparkles, Wand2, AlignLeft, User, MessageSquare, LayoutList } from 'lucide-react';

export default function App() {
  // State untuk menyimpan input pengguna
  const [namaProyek, setNamaProyek] = useState('Proyek Pembangunan Jalan Tol X');
  const [nomorWOSuffix, setNomorWOSuffix] = useState('001');
  const [divisi, setDivisi] = useState('Divisi Infrastruktur 1');
  const [sumberDana, setSumberDana] = useState('APBN');
  const [fungsi, setFungsi] = useState('Membuat COA');
  const [instruksiKhusus, setInstruksiKhusus] = useState('Buatkan jurnal standar akuntansi (Debit/Kredit) setiap kali saya memberikan data transaksi.');
  
  const [format, setFormat] = useState('Tabel Jurnal Akuntansi (Debit/Kredit)');
  
  // State untuk UI
  const [generatedPrompt, setGeneratedPrompt] = useState('');
  const [isCopied, setIsCopied] = useState(false);

  // Kode Prefix untuk masing-masing Divisi
  const kodeDivisi = {
    'Divisi Infrastruktur 1': '100',
    'Divisi Infrastruktur 2': '200',
    'Divisi Properti': '600',
    'Divisi Gedung': '300',
    'Divisi EPC': '500'
  };

  // Daftar opsi untuk dropdown
  const daftarDivisi = [
    'Divisi Infrastruktur 1',
    'Divisi Infrastruktur 2',
    'Divisi Properti',
    'Divisi Gedung',
    'Divisi EPC'
  ];

  const daftarSumberDana = [
    'APBN',
    'APBD',
    'BUMN / Internal',
    'Swasta',
    'Loan / Pinjaman Luar Negeri',
    'KPBU (Kerjasama Pemerintah & Badan Usaha)'
  ];

  const daftarFungsi = [
    'Membuat COA',
    'Membuku PMB',
    'Membuku Klad KAS',
    'Membuku Klad Bank',
    'Membuku MPK',
    'LAINNYA'
  ];

  const formats = [
    'Tabel Jurnal Akuntansi (Debit/Kredit)',
    'Laporan Arus Kas Proyek',
    'Paragraf terstruktur dengan poin-poin',
    'Artikel Blog lengkap (dengan Heading)',
    'Tabel Perbandingan',
    'Skrip Video / Podcast',
    'Kode Pemrograman (dengan penjelasan)',
    'Email Bisnis',
    'Cuitan Twitter / Thread'
  ];

  // Master Template COA Nindya Karya
  const masterCOA = `110.[DIV].[WO]0    KAS PROYEK / KAS KECIL [NAMA PROYEK]
111.[DIV].[WO]0    BANK BNI [NAMA PROYEK] ACC NO. [ISI NOMOR REKENING]
121.[DIV].[WO]0    PIUTANG RETENSI [NAMA PROYEK]
138.[DIV].[WO2][YY]    UANG MUKA / PIUTANG [NAMA PROYEK] (YY = Inisial Suplier)
150.[DIV].[WO]0    TAGIHAN BRUTO (JENIS PROYEK BANGUNAN/GEDUNG) [NAMA PROYEK]
160.[DIV].[WO]8    PPH FINAL [NAMA PROYEK]
200.[DIV].[WO2][YY]    HUTANG BAHAN [NAMA PROYEK] (YY = Inisial Suplier)
201.[DIV].[WO2][YY]    HUTANG UPAH [NAMA PROYEK] (YY = Inisial Mandor/Pekerja)
20A.[DIV].[WO2][YY]    HUTANG PPN MASUKAN [NAMA PROYEK] (YY = Inisial Suplier)
230.[DIV].[WO2]00    UTANG BRUTO BAHAN [NAMA PROYEK]
230.[DIV].[WO2]01    UTANG BRUTO UPAH [NAMA PROYEK]
230.[DIV].[WO2]03    UTANG BRUTO SUBKONTRAKTOR [NAMA PROYEK]
230.[DIV].[WO2]05    UT BRUTO OVHD [NAMA PROYEK]
230.[DIV].[WO2]08    UTANG BRUTO PPH FINAL [NAMA PROYEK]
241.[DIV].[WO2][YY]    HUTANG RETENSI [NAMA PROYEK] (YY = Inisial Subkon/Suplier)
260.[DIV].[WO2]00    POS SILANG KAS-BANK [NAMA PROYEK]
273.[DIV].[WO2]01    DROPING TUNAI PROYEK [NAMA PROYEK]
400.[DIV].[WO]B    PENDAPATAN USAHA KONTRAK INDUK (DANA DARI BUMN) [NAMA PROYEK]
500.[DIV].[WO]0    BIAYA BAHAN [NAMA PROYEK]
500.[DIV].[WO]1    BIAYA BAHAN LAIN-LAIN [NAMA PROYEK]
501.[DIV].[WO]1    BIAYA UPAH BORONGAN [NAMA PROYEK]
501.[DIV].[WO]2    BIAYA UPAH HARIAN [NAMA PROYEK]
502.[DIV].[WO]0    BIAYA PERALATAN [NAMA PROYEK]
502.[DIV].[WO]1    BIAYA SEWA ALAT [NAMA PROYEK]
502.[DIV].[WO]2    BIAYA PERBAIKAN ALAT [NAMA PROYEK]
503.[DIV].[WO]1    BIAYA SUBKONTRAKTOR KONSTRUKSI [NAMA PROYEK]
504.[DIV].[WO]1    BIAYA ADM BANK [NAMA PROYEK]
505.[DIV].[WO]0    BIAYA GAJI KARYAWAN [NAMA PROYEK]
505.[DIV].[WO]1    BIAYA ADMINISTRASI DAN DOKUMENTASI [NAMA PROYEK]
505.[DIV].[WO]2    BIAYA KONSUMSI [NAMA PROYEK]
505.[DIV].[WO]3    BIAYA OPERASIONAL KENDARAAN [NAMA PROYEK]
505.[DIV].[WO]4    BIAYA SEWA RUMAH/MESS/KANTOR [NAMA PROYEK]
505.[DIV].[WO]5    BIAYA PERLENGKAPAN KANTOR/MESS [NAMA PROYEK]
505.[DIV].[WO]6    BIAYA ASTEK/CAR [NAMA PROYEK]
505.[DIV].[WO]8    BIAYA DINAS/SPD/TAMU [NAMA PROYEK]
505.[DIV].[WO]9    BIAYA UPAH KONTRAK PROYEK [NAMA PROYEK]
505.[DIV].[WO]K    BIAYA KESEHATAN, KESELAMATAN, KEAMANAN DAN LINGKUNGAN (K3L) [NAMA PROYEK]
508.[DIV].[WO]0    BIAYA PPH FINAL [NAMA PROYEK]`;

  // Efek untuk mengubah teks instruksi otomatis saat "Fungsi" diganti
  useEffect(() => {
    let instruksiBaru = '';
    switch (fungsi) {
      case 'Membuat COA':
        instruksiBaru = `Tampilkan dan rapikan Referensi Chart of Account (COA) yang saya lampirkan di bawah ini ke dalam bentuk tabel Master Data yang siap dibaca oleh manajemen.`;
        break;
      case 'Membuku PMB':
        instruksiBaru = `Buatkan jurnal akuntansi (Debit/Kredit) khusus untuk transaksi Penerimaan Material di Proyek (PMB) setiap kali saya memberikan datanya.`;
        break;
      case 'Membuku Klad KAS':
        instruksiBaru = `Setiap kali saya memberikan data transaksi kas tunai harian proyek, tugas Anda HANYA membuat Jurnal Akuntansi dengan format teks terstruktur berikut untuk SETIAP transaksi:

Tanggal: [Isi Tanggal Transaksi]
Nomor Bukti: [NomorUrut]/KCC/MM/YY (Ganti [NomorUrut] sesuai data. 'K' adalah kode Kas, 'CC' adalah 2 angka terakhir nomor WO proyek ini, 'MM/YY' adalah bulan dan tahun transaksi)
Keterangan: [Subject/Pihak Terkait] - [Keterangan transaksi] (Sertakan No. PO/Invoice/Kontrak jika ada)

Lalu buatkan tabel di bawahnya HANYA dengan kolom: Kode Akun, Nama Akun, Debit, dan Kredit.

Aturan Tambahan:
- Pisahkan setiap transaksi / Nomor Urut menggunakan susunan format di atas.
- Aturan Khusus "Multi-Item/Rincian": Jika dalam 1 Nomor Urut terdapat beberapa rincian pengeluaran (misalnya: Pertanggungjawaban untuk makan, parkir, bensin), gabungkan rincian tersebut ke dalam SATU tabel jurnal yang sama di bawah satu header Nomor Bukti.
- Aturan Khusus "Direksi Keet": Jika transaksi untuk "Direksi Keet", WAJIB dialokasikan ke kelompok akun 505.
- Aturan Khusus "Pos Silang": Jika ada transaksi tarik tunai dari Bank atau setor tunai ke Bank, WAJIB gunakan akun 260 (Pos Silang Kas-Bank) sebagai akun lawan, BUKAN langsung menggunakan akun Bank.
- Aturan Khusus "Droping Divisi": Jika ada penerimaan dana droping/transfer dari Divisi/Pusat, WAJIB gunakan akun 273 (Droping Tunai Proyek) sebagai akun lawan.
- Gunakan pedoman nomor akun dari Referensi COA standar di bawah.`;
        break;
      case 'Membuku Klad Bank':
        instruksiBaru = `Setiap kali saya memberikan data transaksi rekening koran / mutasi bank proyek, tugas Anda HANYA membuat Jurnal Akuntansi dengan format teks terstruktur berikut untuk SETIAP transaksi:

Tanggal: [Isi Tanggal Transaksi]
Nomor Bukti: [NomorUrut]/BCC/MM/YY (Ganti [NomorUrut] sesuai data. 'B' adalah kode Bank, 'CC' adalah 2 angka terakhir nomor WO proyek ini, 'MM/YY' adalah bulan dan tahun transaksi)
Keterangan: [Subject/Pihak Terkait] - [Keterangan transaksi] (Sertakan No. PO/Invoice/Kontrak jika ada)

Lalu buatkan tabel di bawahnya HANYA dengan kolom: Kode Akun, Nama Akun, Debit, dan Kredit.

Aturan Tambahan:
- Pisahkan setiap transaksi / Nomor Urut menggunakan susunan format di atas.
- Aturan Khusus "Multi-Item/Rincian": Jika dalam 1 Nomor Urut terdapat beberapa rincian, gabungkan rincian tersebut ke dalam SATU tabel jurnal yang sama di bawah satu header Nomor Bukti.
- Aturan Khusus "Pos Silang": Jika ada mutasi penarikan dana ke Kas atau setoran dana dari Kas, WAJIB gunakan akun 260 (Pos Silang Kas-Bank) sebagai akun lawan, BUKAN langsung menggunakan akun Kas.
- Aturan Khusus "Droping Divisi": Jika ada dana masuk berupa droping/transfer dari Divisi/Pusat, WAJIB gunakan akun 273 (Droping Tunai Proyek) sebagai akun lawan.
- Gunakan pedoman nomor akun dari Referensi COA standar di bawah.`;
        break;
      case 'Membuku MPK':
        instruksiBaru = `Buatkan jurnal akuntansi khusus untuk transaksi MPK (Mutasi) setiap kali saya memberikan datanya.`;
        break;
      default:
        instruksiBaru = `Buatkan jurnal standar akuntansi (Debit/Kredit) setiap kali saya memberikan data transaksi.`;
    }
    setInstruksiKhusus(instruksiBaru);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fungsi]);

  // Efek untuk memperbarui prompt setiap kali ada perubahan input
  useEffect(() => {
    generatePrompt();
  }, [namaProyek, nomorWOSuffix, divisi, sumberDana, fungsi, instruksiKhusus, format]);

  const generatePrompt = () => {
    const currentDiv = kodeDivisi[divisi];
    const currentWO = nomorWOSuffix || 'YYY';
    
    // Logika khusus: Ambil 2 digit terakhir dari WO untuk akun seri 230, 138, 200, dll.
    const currentWO2 = nomorWOSuffix ? nomorWOSuffix.padStart(3, '0').slice(-2) : 'YY';
    
    const currentProyekName = namaProyek ? namaProyek.toUpperCase() : 'NAMA PROYEK';
    const fullNomorWO = `${currentDiv}-${currentWO}`;
    
    // Merakit COA dengan me-replace variabel
    const processedCOA = masterCOA
      .replaceAll('[DIV]', currentDiv)
      .replaceAll('[WO]', currentWO)
      .replaceAll('[WO2]', currentWO2)
      .replaceAll('[NAMA PROYEK]', currentProyekName);

    const isCOA = fungsi === 'Membuat COA';
    const isKladKas = fungsi === 'Membuku Klad KAS';
    const isKladBank = fungsi === 'Membuku Klad Bank';
    
    let formatOutputText = '';
    if (isCOA) {
      formatOutputText = 'Berikan HANYA tabel sederhana berisi daftar Chart of Account (COA) saja agar mudah di-copy ke dalam Sistem Informasi Akuntansi (ERP). JANGAN menggunakan format markdown yang rumit, teks pengantar, sapaan, penjelasan, atau penutup apa pun.';
    } else if (isKladKas || isKladBank) {
      formatOutputText = 'Ikuti struktur penulisan Tanggal, Nomor Bukti, dan Keterangan DI LUAR TABEL, lalu diikuti tabel penjurnalan murni (Kode Akun, Nama Akun, Debit, Kredit) untuk setiap transaksi.';
    } else {
      formatOutputText = `Berikan setiap jawaban Anda dalam bentuk ${format}.`;
    }

    // Aturan khusus tambahan untuk AI mengerti maksud [YY]
    const formatCOAContext = `\n- Aturan Khusus Penomoran Dinamis: 
  Jika Anda melihat kode akun yang berakhiran "[YY]" (seperti 138, 200, 201, 20A, 241), Anda WAJIB mengganti "[YY]" dengan 1 atau 2 HURUF INISIAL dari nama pihak yang bersangkutan. 
  Contoh: Jika menjurnal Hutang Retensi untuk "Ahmad Bahrul Munir", maka "241.${currentDiv}.${currentWO2}[YY]" harus menjadi "241.${currentDiv}.${currentWO2}AB".`;

    const closingText = isCOA 
      ? `Silakan langsung tampilkan tabel sederhana Chart of Account (COA) tersebut sekarang berdasarkan data referensi di atas tanpa basa-basi.`
      : `Jika Anda sudah paham dengan instruksi dan konteks di atas, jawablah dengan: \n"Saya siap! Silakan masukkan data transaksi yang ingin dibukukan." \n\n(Penting: Jangan membuat output pembukuan apa pun sebelum saya memberikan datanya).`;

    const promptTemplate = `Anda ditugaskan untuk menangani pembukuan dan penjurnalan akuntansi untuk:
- Perusahaan: PT Nindya Karya
- Nama Proyek: ${namaProyek || '[Nama Proyek]'}
- Divisi: ${divisi || '[Divisi]'}
- Sumber Dana: ${sumberDana || '[Sumber Dana]'}
- Nomor WO: ${fullNomorWO}
- Fungsi/Tugas Spesifik: ${fungsi || '[Fungsi]'}

Tugas Utama Anda:
${instruksiKhusus || 'Buatkan jurnal akuntansi untuk transaksi yang akan diberikan.'}

Konteks & Aturan Tambahan:
- Format Output: ${formatOutputText}${formatCOAContext}

REFERENSI CHART OF ACCOUNT (COA) STANDAR:
Berikut adalah master data akun yang WAJIB Anda gunakan. Jangan membuat kode akun di luar daftar ini kecuali benar-benar diperlukan.
--------------------------------------------------
${processedCOA}
--------------------------------------------------

${closingText}`;

    setGeneratedPrompt(promptTemplate);
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(generatedPrompt);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (err) {
      // Fallback jika clipboard API gagal
      const textArea = document.createElement("textarea");
      textArea.value = generatedPrompt;
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
      } catch (err) {
        console.error('Gagal menyalin', err);
      }
      document.body.removeChild(textArea);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 font-sans selection:bg-blue-200">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-8 px-6 shadow-md">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <Sparkles className="h-8 w-8 text-yellow-300" />
              Generator Prompt Akuntansi
            </h1>
            <p className="mt-2 text-blue-100 opacity-90 text-lg">
              Sistem pembuat instruksi AI khusus untuk pembukuan proyek PT Nindya Karya.
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto p-6 mt-6 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Inputs (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 text-slate-800">
              <AlignLeft className="h-5 w-5 text-blue-600" />
              1. Informasi Proyek
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Nama Proyek</label>
                <input
                  type="text"
                  className="w-full p-3 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none"
                  placeholder="Contoh: Proyek Bendungan..."
                  value={namaProyek}
                  onChange={(e) => setNamaProyek(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Divisi</label>
                <select
                  className="w-full p-3 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition-all outline-none cursor-pointer"
                  value={divisi}
                  onChange={(e) => setDivisi(e.target.value)}
                >
                  {daftarDivisi.map((d) => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Sumber Dana</label>
                <select
                  className="w-full p-3 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition-all outline-none cursor-pointer"
                  value={sumberDana}
                  onChange={(e) => setSumberDana(e.target.value)}
                >
                  {daftarSumberDana.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Nomor WO (XXX-YYY)</label>
                <div className="flex items-center gap-3">
                  <input
                    type="text"
                    className="w-24 p-3 bg-slate-200 border border-slate-300 rounded-lg text-center font-bold text-slate-700 outline-none cursor-not-allowed"
                    value={kodeDivisi[divisi]}
                    disabled
                    title="Kode otomatis berdasarkan Divisi"
                  />
                  <span className="text-slate-400 font-bold text-xl">-</span>
                  <input
                    type="text"
                    maxLength="3"
                    className="flex-1 p-3 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none"
                    placeholder="Contoh: 001"
                    value={nomorWOSuffix}
                    onChange={(e) => setNomorWOSuffix(e.target.value.replace(/\D/g, ''))}
                  />
                </div>
                <p className="text-xs text-slate-500 mt-1">3 digit pertama otomatis mengikuti Divisi, masukkan 3 digit terakhir.</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Fungsi</label>
                <select
                  className="w-full p-3 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition-all outline-none cursor-pointer"
                  value={fungsi}
                  onChange={(e) => setFungsi(e.target.value)}
                >
                  {daftarFungsi.map((f) => (
                    <option key={f} value={f}>{f}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Instruksi / Tugas</label>
                <textarea
                  className="w-full h-32 p-3 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all resize-none text-slate-700 outline-none"
                  placeholder="Instruksi spesifik untuk AI..."
                  value={instruksiKhusus}
                  onChange={(e) => setInstruksiKhusus(e.target.value)}
                />
              </div>
            </div>
          </div>

          {!['Membuat COA', 'Membuku Klad KAS', 'Membuku Klad Bank'].includes(fungsi) && (
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
              <h2 className="text-xl font-semibold mb-6 flex items-center gap-2 text-slate-800">
                <Wand2 className="h-5 w-5 text-blue-600" />
                2. Kustomisasi Parameter
              </h2>
              
              <div className="grid grid-cols-1 gap-5">
                {/* Format */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700 flex items-center gap-1.5">
                    <LayoutList className="h-4 w-4" /> Format Hasil
                  </label>
                  <select 
                    className="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={format}
                    onChange={(e) => setFormat(e.target.value)}
                  >
                    {formats.map((f) => <option key={f} value={f}>{f}</option>)}
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Output Preview (5 cols) */}
        <div className="lg:col-span-5 relative">
          <div className="bg-slate-800 text-slate-100 p-6 rounded-2xl shadow-xl sticky top-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-blue-300">Hasil Prompt:</h2>
              <button 
                onClick={copyToClipboard}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                  isCopied 
                    ? 'bg-green-500 hover:bg-green-600 text-white' 
                    : 'bg-blue-600 hover:bg-blue-500 text-white'
                }`}
              >
                {isCopied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                {isCopied ? 'Tersalin!' : 'Salin Prompt'}
              </button>
            </div>
            
            <div className="bg-slate-900 rounded-xl p-5 border border-slate-700">
              <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-slate-300">
                {generatedPrompt}
              </pre>
            </div>
            
            <div className="mt-5 text-sm text-slate-400 bg-slate-800/50 p-3 rounded-lg border border-slate-700">
              💡 <strong>Tips:</strong> Salin teks di atas dan tempelkan (paste) ke kolom obrolan <a href="https://gemini.google.com" target="_blank" rel="noreferrer" className="text-blue-400 hover:underline">Gemini</a> untuk melihat hasilnya.
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}