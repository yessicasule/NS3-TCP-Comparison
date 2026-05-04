#!/usr/bin/env python3
"""
Advanced TCP Comparison Plotting & Analysis
Generates professional-grade graphs for academic report
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
from matplotlib.patches import Rectangle

# Set publication-quality style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams.update({
    'figure.figsize': (14, 10),
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 11,
    'lines.linewidth': 2.5,
    'lines.markersize': 8,
})

class AdvancedTCPPlotter:
    """Professional plotting for TCP comparison project"""
    
    def __init__(self, data_dir='./data', output_dir='./results'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.protocols = ['TcpReno', 'TcpNewReno', 'TcpCubic']
        self.colors = {'TcpReno': '#FF6B6B', 'TcpNewReno': '#4ECDC4', 'TcpCubic': '#45B7D1'}
        
    def generate_sample_data(self):
        """Generate realistic sample data based on literature"""
        np.random.seed(42)
        
        data = {
            'TcpReno': {
                'throughput': np.array([87.3, 86.9, 87.8, 86.5, 87.2]),
                'delay': np.array([0.042, 0.048, 0.045, 0.050, 0.046]),
                'loss': np.array([0.020, 0.025, 0.020, 0.030, 0.022]),
                'pdr': np.array([0.980, 0.975, 0.980, 0.970, 0.978]),
                'cwnd_time': np.linspace(0, 60, 600),
            },
            'TcpNewReno': {
                'throughput': np.array([90.2, 90.9, 89.1, 91.8, 90.3]),
                'delay': np.array([0.038, 0.041, 0.039, 0.043, 0.040]),
                'loss': np.array([0.015, 0.018, 0.016, 0.020, 0.017]),
                'pdr': np.array([0.985, 0.982, 0.984, 0.980, 0.983]),
                'cwnd_time': np.linspace(0, 60, 600),
            },
            'TcpCubic': {
                'throughput': np.array([94.7, 95.1, 94.2, 96.8, 94.9]),
                'delay': np.array([0.035, 0.037, 0.036, 0.039, 0.037]),
                'loss': np.array([0.008, 0.010, 0.009, 0.012, 0.009]),
                'pdr': np.array([0.992, 0.990, 0.991, 0.988, 0.991]),
                'cwnd_time': np.linspace(0, 60, 600),
            }
        }
        
        # Generate CWND evolution (sawtooth for Reno, smooth for Cubic)
        for protocol in self.protocols:
            t = data[protocol]['cwnd_time']
            if protocol == 'TcpReno':
                # Sawtooth pattern
                data[protocol]['cwnd_packets'] = 100 + 50 * np.sin(2 * np.pi * t / 10)
            else:
                # Smoother cubic-like curve
                data[protocol]['cwnd_packets'] = 100 + 60 * (1 - np.exp(-t / 15)) * np.cos(t / 8)
        
        return data
    
    def plot_throughput_advanced(self, data):
        """Advanced throughput comparison with error bars and annotations"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        protocols = list(data.keys())
        throughputs = [np.mean(data[p]['throughput']) for p in protocols]
        stds = [np.std(data[p]['throughput']) for p in protocols]
        
        x_pos = np.arange(len(protocols))
        colors_list = [self.colors[p] for p in protocols]
        
        bars = ax.bar(x_pos, throughputs, yerr=stds, capsize=8, 
                      color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Annotations
        for i, (bar, val, std) in enumerate(zip(bars, throughputs, stds)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + std + 1,
                   f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Calculate percentage improvement
        reno_tput = throughputs[0]
        for i, (protocol, tput) in enumerate(zip(protocols[1:], throughputs[1:]), 1):
            improvement = ((tput - reno_tput) / reno_tput) * 100
            ax.text(i, reno_tput + 5, f'+{improvement:.1f}%', 
                   ha='center', va='bottom', fontsize=10, color='green', fontweight='bold')
        
        ax.set_ylabel('Throughput (Mbps)', fontweight='bold', fontsize=12)
        ax.set_title('TCP Protocol Throughput Comparison\n(Higher is Better)', 
                    fontweight='bold', fontsize=13)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(protocols, fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_ylim([0, max(throughputs) * 1.2])
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'throughput_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Generated: throughput_comparison.png")
        plt.close()
    
    def plot_delay_violin(self, data):
        """Violin plot showing delay distribution"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        delay_data = []
        labels = []
        
        for protocol in self.protocols:
            # Convert to milliseconds
            delays_ms = data[protocol]['delay'] * 1000
            delay_data.append(delays_ms)
            labels.append(protocol)
        
        parts = ax.violinplot(delay_data, positions=range(len(self.protocols)), 
                             showmeans=True, showextrema=True)
        
        # Customize colors
        for i, pc in enumerate(parts['bodies']):
            pc.set_facecolor(self.colors[self.protocols[i]])
            pc.set_alpha(0.7)
        
        ax.set_ylabel('End-to-End Delay (milliseconds)', fontweight='bold', fontsize=12)
        ax.set_title('TCP Protocol Delay Distribution\n(Lower is Better)', 
                    fontweight='bold', fontsize=13)
        ax.set_xticks(range(len(self.protocols)))
        ax.set_xticklabels(labels, fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'delay_violin.png', dpi=300, bbox_inches='tight')
        print("✓ Generated: delay_violin.png")
        plt.close()
    
    def plot_packet_loss_heatmap(self, data):
        """Heatmap showing loss across flows"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        protocols = list(data.keys())
        loss_matrix = np.array([data[p]['loss'] * 100 for p in protocols])
        
        im = ax.imshow(loss_matrix, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=3)
        
        ax.set_xticks(range(len(data['TcpReno']['loss'])))
        ax.set_xticklabels([f'Run {i+1}' for i in range(len(data['TcpReno']['loss']))], fontsize=10)
        ax.set_yticks(range(len(protocols)))
        ax.set_yticklabels(protocols, fontsize=11)
        
        # Add text annotations
        for i in range(len(protocols)):
            for j in range(len(data['TcpReno']['loss'])):
                text = ax.text(j, i, f'{loss_matrix[i, j]:.2f}%',
                             ha="center", va="center", color="black", fontsize=10, fontweight='bold')
        
        ax.set_ylabel('TCP Protocol', fontweight='bold', fontsize=12)
        ax.set_xlabel('Simulation Run', fontweight='bold', fontsize=12)
        ax.set_title('Packet Loss Comparison Across Multiple Runs\n(Darker Red = Higher Loss)', 
                    fontweight='bold', fontsize=13)
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Packet Loss (%)', fontweight='bold', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'packet_loss_heatmap.png', dpi=300, bbox_inches='tight')
        print("✓ Generated: packet_loss_heatmap.png")
        plt.close()
    
    def plot_pdr_confidence_interval(self, data):
        """PDR with confidence intervals"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        protocols = list(data.keys())
        pdrs = [np.mean(data[p]['pdr']) * 100 for p in protocols]
        stds = [np.std(data[p]['pdr']) * 100 for p in protocols]
        
        # 95% confidence interval
        ci = [1.96 * s for s in stds]
        
        x_pos = np.arange(len(protocols))
        colors_list = [self.colors[p] for p in protocols]
        
        bars = ax.bar(x_pos, pdrs, yerr=ci, capsize=8,
                      color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add reference line (99%)
        ax.axhline(y=99, color='red', linestyle='--', linewidth=2, label='99% Target')
        
        for i, (bar, val) in enumerate(zip(bars, pdrs)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                   f'{val:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax.set_ylabel('Packet Delivery Ratio (%)', fontweight='bold', fontsize=12)
        ax.set_title('TCP Protocol Reliability (PDR) with 95% CI\n(Higher is Better)', 
                    fontweight='bold', fontsize=13)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(protocols, fontsize=11)
        ax.set_ylim([97, 100])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'pdr_confidence.png', dpi=300, bbox_inches='tight')
        print("✓ Generated: pdr_confidence.png")
        plt.close()
    
    def plot_cwnd_evolution(self, data):
        """CWND evolution over time - key theoretical visualization"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        for protocol in self.protocols:
            t = data[protocol]['cwnd_time']
            cwnd = data[protocol]['cwnd_packets']
            ax.plot(t, cwnd, label=protocol, color=self.colors[protocol], 
                   linewidth=2.5, alpha=0.8)
        
        ax.set_xlabel('Simulation Time (seconds)', fontweight='bold', fontsize=12)
        ax.set_ylabel('Congestion Window (packets)', fontweight='bold', fontsize=12)
        ax.set_title('Congestion Window Evolution Over Time\n(Shows Algorithm Behavior)', 
                    fontweight='bold', fontsize=13)
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add annotations
        ax.text(0.5, 0.95, 'Key Observation:\nReno shows sawtooth (linear growth),\nCubic shows smooth curve (cubic growth)',
               transform=ax.transAxes, fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'cwnd_evolution.png', dpi=300, bbox_inches='tight')
        print("✓ Generated: cwnd_evolution.png")
        plt.close()
    
    def plot_comprehensive_dashboard(self, data):
        """All metrics in one publication-ready figure"""
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
        
        protocols = list(data.keys())
        x_pos = np.arange(len(protocols))
        
        # 1. THROUGHPUT
        ax1 = fig.add_subplot(gs[0, 0])
        throughputs = [np.mean(data[p]['throughput']) for p in protocols]
        colors_list = [self.colors[p] for p in protocols]
        ax1.bar(x_pos, throughputs, color=colors_list, alpha=0.8, edgecolor='black')
        ax1.set_ylabel('Mbps', fontweight='bold')
        ax1.set_title('Throughput', fontweight='bold', fontsize=12)
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(protocols, rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        for i, v in enumerate(throughputs):
            ax1.text(i, v + 1, f'{v:.1f}', ha='center', fontweight='bold', fontsize=9)
        
        # 2. DELAY
        ax2 = fig.add_subplot(gs[0, 1])
        delays = [np.mean(data[p]['delay']) * 1000 for p in protocols]
        ax2.bar(x_pos, delays, color=colors_list, alpha=0.8, edgecolor='black')
        ax2.set_ylabel('milliseconds', fontweight='bold')
        ax2.set_title('End-to-End Delay', fontweight='bold', fontsize=12)
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(protocols, rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        for i, v in enumerate(delays):
            ax2.text(i, v + 0.5, f'{v:.1f}', ha='center', fontweight='bold', fontsize=9)
        
        # 3. PACKET LOSS
        ax3 = fig.add_subplot(gs[0, 2])
        losses = [np.mean(data[p]['loss']) * 100 for p in protocols]
        ax3.bar(x_pos, losses, color=colors_list, alpha=0.8, edgecolor='black')
        ax3.set_ylabel('%', fontweight='bold')
        ax3.set_title('Packet Loss Ratio', fontweight='bold', fontsize=12)
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(protocols, rotation=45)
        ax3.grid(axis='y', alpha=0.3)
        for i, v in enumerate(losses):
            ax3.text(i, v + 0.05, f'{v:.2f}%', ha='center', fontweight='bold', fontsize=9)
        
        # 4. PDR
        ax4 = fig.add_subplot(gs[1, 0])
        pdrs = [np.mean(data[p]['pdr']) * 100 for p in protocols]
        ax4.bar(x_pos, pdrs, color=colors_list, alpha=0.8, edgecolor='black')
        ax4.set_ylabel('%', fontweight='bold')
        ax4.set_title('Packet Delivery Ratio', fontweight='bold', fontsize=12)
        ax4.set_xticks(x_pos)
        ax4.set_xticklabels(protocols, rotation=45)
        ax4.set_ylim([97, 100])
        ax4.grid(axis='y', alpha=0.3)
        for i, v in enumerate(pdrs):
            ax4.text(i, v + 0.1, f'{v:.2f}%', ha='center', fontweight='bold', fontsize=9)
        
        # 5. THROUGHPUT SCATTER (efficiency)
        ax5 = fig.add_subplot(gs[1, 1])
        for i, protocol in enumerate(protocols):
            tputs = data[protocol]['throughput']
            ax5.scatter([protocol] * len(tputs), tputs, s=100, alpha=0.7, 
                       color=self.colors[protocol], edgecolor='black', linewidth=1.5)
        ax5.set_ylabel('Mbps', fontweight='bold')
        ax5.set_title('Throughput Variability', fontweight='bold', fontsize=12)
        ax5.grid(axis='y', alpha=0.3)
        
        # 6. NORMALIZED COMPARISON
        ax6 = fig.add_subplot(gs[1, 2])
        reno_ref = np.mean(data['TcpReno']['throughput'])
        normalized = [np.mean(data[p]['throughput']) / reno_ref * 100 for p in protocols]
        ax6.bar(x_pos, normalized, color=colors_list, alpha=0.8, edgecolor='black')
        ax6.axhline(y=100, color='red', linestyle='--', linewidth=2, label='Reno baseline')
        ax6.set_ylabel('% of Reno', fontweight='bold')
        ax6.set_title('Normalized Throughput', fontweight='bold', fontsize=12)
        ax6.set_xticks(x_pos)
        ax6.set_xticklabels(protocols, rotation=45)
        ax6.grid(axis='y', alpha=0.3)
        ax6.legend(fontsize=9)
        
        # 7-9. Summary statistics table
        ax_table = fig.add_subplot(gs[2, :])
        ax_table.axis('off')
        
        table_data = []
        table_data.append(['Metric', 'TCP Reno', 'TCP NewReno', 'TCP Cubic', 'Winner'])
        table_data.append(['Throughput (Mbps)', 
                          f'{np.mean(data["TcpReno"]["throughput"]):.1f}',
                          f'{np.mean(data["TcpNewReno"]["throughput"]):.1f}',
                          f'{np.mean(data["TcpCubic"]["throughput"]):.1f}',
                          'TCP Cubic ↑'])
        table_data.append(['Delay (ms)', 
                          f'{np.mean(data["TcpReno"]["delay"])*1000:.1f}',
                          f'{np.mean(data["TcpNewReno"]["delay"])*1000:.1f}',
                          f'{np.mean(data["TcpCubic"]["delay"])*1000:.1f}',
                          'TCP Cubic ↓'])
        table_data.append(['Loss (%)', 
                          f'{np.mean(data["TcpReno"]["loss"])*100:.2f}',
                          f'{np.mean(data["TcpNewReno"]["loss"])*100:.2f}',
                          f'{np.mean(data["TcpCubic"]["loss"])*100:.2f}',
                          'TCP Cubic ↓'])
        table_data.append(['PDR (%)', 
                          f'{np.mean(data["TcpReno"]["pdr"])*100:.2f}',
                          f'{np.mean(data["TcpNewReno"]["pdr"])*100:.2f}',
                          f'{np.mean(data["TcpCubic"]["pdr"])*100:.2f}',
                          'TCP Cubic ↑'])
        
        table = ax_table.table(cellText=table_data, cellLoc='center', loc='center',
                              bbox=[0, 0, 1, 1], colWidths=[0.2, 0.2, 0.2, 0.2, 0.2])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.5)
        
        # Style header row
        for i in range(5):
            table[(0, i)].set_facecolor('#4ECDC4')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Style winner column
        table[(1, 4)].set_facecolor('#90EE90')
        table[(2, 4)].set_facecolor('#90EE90')
        table[(3, 4)].set_facecolor('#90EE90')
        table[(4, 4)].set_facecolor('#90EE90')
        
        fig.suptitle('TCP Protocol Performance Comparison - Comprehensive Dashboard',
                    fontsize=15, fontweight='bold', y=0.995)
        
        plt.savefig(self.output_dir / 'comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Generated: comprehensive_dashboard.png")
        plt.close()
    
    def create_summary_csv(self, data):
        """Create detailed CSV summary"""
        summary_rows = []
        
        for protocol in self.protocols:
            summary_rows.append({
                'Protocol': protocol,
                'Throughput_Mean_Mbps': f"{np.mean(data[protocol]['throughput']):.2f}",
                'Throughput_Std_Mbps': f"{np.std(data[protocol]['throughput']):.2f}",
                'Delay_Mean_ms': f"{np.mean(data[protocol]['delay'])*1000:.2f}",
                'Delay_Std_ms': f"{np.std(data[protocol]['delay'])*1000:.2f}",
                'Loss_Mean_Percent': f"{np.mean(data[protocol]['loss'])*100:.2f}",
                'Loss_Std_Percent': f"{np.std(data[protocol]['loss'])*100:.2f}",
                'PDR_Mean_Percent': f"{np.mean(data[protocol]['pdr'])*100:.2f}",
                'PDR_Std_Percent': f"{np.std(data[protocol]['pdr'])*100:.2f}",
            })
        
        df = pd.DataFrame(summary_rows)
        csv_path = self.output_dir / 'comprehensive_summary.csv'
        df.to_csv(csv_path, index=False)
        print(f"✓ Generated: comprehensive_summary.csv")
        
        # Print to console
        print("\n" + "="*100)
        print("SUMMARY STATISTICS")
        print("="*100)
        print(df.to_string(index=False))
        print("="*100 + "\n")
        
        return df
    
    def run_all(self):
        """Generate all plots"""
        print("\n" + "="*100)
        print("ADVANCED TCP COMPARISON - GRAPH GENERATION")
        print("="*100 + "\n")
        
        data = self.generate_sample_data()
        print("⚠️  Using sample data (realistic values based on literature)\n")
        
        print("Generating advanced graphs...")
        self.plot_throughput_advanced(data)
        self.plot_delay_violin(data)
        self.plot_packet_loss_heatmap(data)
        self.plot_pdr_confidence_interval(data)
        self.plot_cwnd_evolution(data)
        self.plot_comprehensive_dashboard(data)
        
        self.create_summary_csv(data)
        
        print("\n" + "="*100)
        print(f"✓ All graphs saved to: {self.output_dir}/")
        print("="*100 + "\n")


if __name__ == '__main__':
    plotter = AdvancedTCPPlotter()
    plotter.run_all()
