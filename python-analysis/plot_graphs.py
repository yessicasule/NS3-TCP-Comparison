#!/usr/bin/env python3
"""
Plot graphs from NS-3 TCP simulation results
Visualizes throughput, delay, PDR, and packet loss
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

class TCPSimulationPlotter:
    def __init__(self, data_dir='./data', output_dir='./results'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.protocols = ['TcpReno', 'TcpNewReno', 'TcpCubic']
        self.metrics = ['Throughput', 'Delay', 'Loss', 'PDR']
        
    def read_metrics(self):
        """Read metrics from simulation output files"""
        data = {}
        
        for protocol in self.protocols:
            filename = self.data_dir / f"{protocol}-metrics.txt"
            if filename.exists():
                df = pd.read_csv(filename, names=['Protocol', 'Throughput', 'Delay', 'Loss', 'PDR'])
                data[protocol] = {
                    'throughput': df['Throughput'].values,
                    'delay': df['Delay'].values,
                    'loss': df['Loss'].values,
                    'pdr': df['PDR'].values
                }
        
        return data
    
    def generate_sample_data(self):
        """Generate sample data for demonstration (when no real data exists)"""
        print("⚠️  No real data found. Generating sample data for demonstration...")
        
        # Simulated realistic metrics
        data = {
            'TcpReno': {
                'throughput': np.array([87.5, 85.2, 88.1, 86.9, 87.3]),
                'delay': np.array([0.042, 0.048, 0.045, 0.050, 0.046]),
                'loss': np.array([0.02, 0.025, 0.020, 0.030, 0.022]),
                'pdr': np.array([0.98, 0.975, 0.98, 0.97, 0.978])
            },
            'TcpNewReno': {
                'throughput': np.array([89.5, 91.2, 90.1, 92.3, 90.8]),
                'delay': np.array([0.038, 0.041, 0.039, 0.043, 0.040]),
                'loss': np.array([0.015, 0.018, 0.016, 0.020, 0.017]),
                'pdr': np.array([0.985, 0.982, 0.984, 0.980, 0.983])
            },
            'TcpCubic': {
                'throughput': np.array([93.7, 95.2, 94.1, 96.8, 94.9]),
                'delay': np.array([0.035, 0.037, 0.036, 0.039, 0.037]),
                'loss': np.array([0.008, 0.010, 0.009, 0.012, 0.009]),
                'pdr': np.array([0.992, 0.990, 0.991, 0.988, 0.991])
            }
        }
        
        return data
    
    def plot_throughput_comparison(self, data):
        """Plot throughput comparison"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(self.protocols))
        width = 0.25
        
        throughputs = [np.mean(data[p]['throughput']) for p in self.protocols]
        errors = [np.std(data[p]['throughput']) for p in self.protocols]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bars = ax.bar(x, throughputs, width, yerr=errors, label='Average', 
                      color=colors, alpha=0.8, capsize=5)
        
        ax.set_xlabel('TCP Protocol', fontsize=12, fontweight='bold')
        ax.set_ylabel('Throughput (Mbps)', fontsize=12, fontweight='bold')
        ax.set_title('TCP Protocol Throughput Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(self.protocols)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, throughputs)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + errors[i] + 1,
                   f'{val:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'throughput_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: throughput_comparison.png")
        plt.close()
    
    def plot_delay_comparison(self, data):
        """Plot end-to-end delay comparison"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(self.protocols))
        width = 0.25
        
        delays = [np.mean(data[p]['delay']) * 1000 for p in self.protocols]  # Convert to ms
        errors = [np.std(data[p]['delay']) * 1000 for p in self.protocols]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bars = ax.bar(x, delays, width, yerr=errors, label='Average',
                      color=colors, alpha=0.8, capsize=5)
        
        ax.set_xlabel('TCP Protocol', fontsize=12, fontweight='bold')
        ax.set_ylabel('End-to-End Delay (ms)', fontsize=12, fontweight='bold')
        ax.set_title('TCP Protocol End-to-End Delay Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(self.protocols)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, delays)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + errors[i] + 0.5,
                   f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'delay_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: delay_comparison.png")
        plt.close()
    
    def plot_packet_loss_comparison(self, data):
        """Plot packet loss comparison"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(self.protocols))
        width = 0.25
        
        losses = [np.mean(data[p]['loss']) * 100 for p in self.protocols]  # Convert to %
        errors = [np.std(data[p]['loss']) * 100 for p in self.protocols]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bars = ax.bar(x, losses, width, yerr=errors, label='Average',
                      color=colors, alpha=0.8, capsize=5)
        
        ax.set_xlabel('TCP Protocol', fontsize=12, fontweight='bold')
        ax.set_ylabel('Packet Loss (%)', fontsize=12, fontweight='bold')
        ax.set_title('TCP Protocol Packet Loss Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(self.protocols)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, losses)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + errors[i] + 0.05,
                   f'{val:.2f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'packet_loss_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: packet_loss_comparison.png")
        plt.close()
    
    def plot_pdr_comparison(self, data):
        """Plot Packet Delivery Ratio comparison"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(self.protocols))
        width = 0.25
        
        pdrs = [np.mean(data[p]['pdr']) * 100 for p in self.protocols]  # Convert to %
        errors = [np.std(data[p]['pdr']) * 100 for p in self.protocols]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bars = ax.bar(x, pdrs, width, yerr=errors, label='Average',
                      color=colors, alpha=0.8, capsize=5)
        
        ax.set_xlabel('TCP Protocol', fontsize=12, fontweight='bold')
        ax.set_ylabel('Packet Delivery Ratio (%)', fontsize=12, fontweight='bold')
        ax.set_title('TCP Protocol PDR Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(self.protocols)
        ax.set_ylim([97, 100])
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, pdrs)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + errors[i] + 0.05,
                   f'{val:.2f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'pdr_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: pdr_comparison.png")
        plt.close()
    
    def plot_all_metrics_comparison(self, data):
        """Plot all metrics in one comprehensive figure"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('TCP Protocol Performance Comparison', fontsize=16, fontweight='bold', y=0.995)
        
        x = np.arange(len(self.protocols))
        width = 0.25
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        # Throughput
        throughputs = [np.mean(data[p]['throughput']) for p in self.protocols]
        ax1.bar(x, throughputs, color=colors, alpha=0.8)
        ax1.set_ylabel('Throughput (Mbps)', fontweight='bold')
        ax1.set_title('Throughput', fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(self.protocols)
        ax1.grid(axis='y', alpha=0.3)
        
        # Delay
        delays = [np.mean(data[p]['delay']) * 1000 for p in self.protocols]
        ax2.bar(x, delays, color=colors, alpha=0.8)
        ax2.set_ylabel('Delay (ms)', fontweight='bold')
        ax2.set_title('End-to-End Delay', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(self.protocols)
        ax2.grid(axis='y', alpha=0.3)
        
        # Packet Loss
        losses = [np.mean(data[p]['loss']) * 100 for p in self.protocols]
        ax3.bar(x, losses, color=colors, alpha=0.8)
        ax3.set_ylabel('Loss (%)', fontweight='bold')
        ax3.set_title('Packet Loss', fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(self.protocols)
        ax3.grid(axis='y', alpha=0.3)
        
        # PDR
        pdrs = [np.mean(data[p]['pdr']) * 100 for p in self.protocols]
        ax4.bar(x, pdrs, color=colors, alpha=0.8)
        ax4.set_ylabel('PDR (%)', fontweight='bold')
        ax4.set_title('Packet Delivery Ratio', fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(self.protocols)
        ax4.set_ylim([97, 100])
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'all_metrics_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: all_metrics_comparison.png")
        plt.close()
    
    def create_summary_table(self, data):
        """Create summary table of all metrics"""
        summary_data = []
        
        for protocol in self.protocols:
            summary_data.append({
                'Protocol': protocol,
                'Throughput (Mbps)': f"{np.mean(data[protocol]['throughput']):.2f} ± {np.std(data[protocol]['throughput']):.2f}",
                'Delay (ms)': f"{np.mean(data[protocol]['delay']) * 1000:.2f} ± {np.std(data[protocol]['delay']) * 1000:.2f}",
                'Loss (%)': f"{np.mean(data[protocol]['loss']) * 100:.2f} ± {np.std(data[protocol]['loss']) * 100:.2f}",
                'PDR (%)': f"{np.mean(data[protocol]['pdr']) * 100:.2f} ± {np.std(data[protocol]['pdr']) * 100:.2f}"
            })
        
        df = pd.DataFrame(summary_data)
        print("\n" + "="*80)
        print("SIMULATION RESULTS SUMMARY")
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)
        
        # Save to CSV
        df.to_csv(self.output_dir / 'summary_results.csv', index=False)
        print("✓ Saved: summary_results.csv\n")
    
    def run(self):
        """Run all plotting functions"""
        print("\n" + "="*80)
        print("TCP SIMULATION PLOTTER")
        print("="*80)
        
        # Try to read real data, fall back to sample data
        data = self.read_metrics()
        if not data:
            data = self.generate_sample_data()
        
        print("\nGenerating graphs...")
        self.plot_throughput_comparison(data)
        self.plot_delay_comparison(data)
        self.plot_packet_loss_comparison(data)
        self.plot_pdr_comparison(data)
        self.plot_all_metrics_comparison(data)
        
        # Create summary table
        self.create_summary_table(data)
        
        print(f"✓ All graphs saved to: {self.output_dir}/")
        print("="*80 + "\n")


if __name__ == '__main__':
    plotter = TCPSimulationPlotter(data_dir='./data', output_dir='./results')
    plotter.run()
