import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="AI Book on ROS 2 Fundamentals for Humanoid Robotics">
      <header className={clsx('hero hero--primary', 'bg-primary')}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className="text--center padding-horiz--md">
            <p>A Practical Textbook for the Future of Intelligence and Robotics.</p>
          </div>
          <div className="text--center">
            <Link
              className="button button--secondary button--lg"
              to="/docs/ros2-humanoid-fundamentals/intro-to-ros2">
              Start Reading Textbook
            </Link>
          </div>
        </div>
      </header>
      <main>
        <section className="padding-vert--xl">
          <div className="container">
            <div className="row">
              <div className="col col--4 margin-vert--md">
                <h2>🤖 Introduction to ROS 2</h2>
                <p>Understand what ROS 2 is and why it matters specifically for humanoid robotics. Learn about Distributed Data Service (DDS) concepts that underpin ROS 2's communication model.</p>
                <Link
                  className="button button--primary button--outline"
                  to="/docs/ros2-humanoid-fundamentals/intro-to-ros2">
                  Read Introduction
                </Link>
              </div>
              <div className="col col--4 margin-vert--md">
                <h2>📡 Communication Model</h2>
                <p>Master the core communication patterns in ROS 2: nodes, topics, services, and actions. Learn to implement basic reply-based controller flows for humanoid robots.</p>
                <Link
                  className="button button--primary button--outline"
                  to="/docs/ros2-humanoid-fundamentals/communication-model">
                  Learn Communication
                </Link>
              </div>
              <div className="col col--4 margin-vert--md">
                <h2>🏗️ Robot Structure with URDF</h2>
                <p>Define humanoid robot structure using Unified Robot Description Format (URDF) for simulation readiness and proper kinematic representation.</p>
                <Link
                  className="button button--primary button--outline"
                  to="/docs/ros2-humanoid-fundamentals/robot-structure-urdf">
                  Understand URDF
                </Link>
              </div>
            </div>
          </div>
        </section>
        <section className="padding-vert--lg bg-gray-100">
          <div className="container">
            <div className="row">
              <div className="col">
                <h2>🎯 About This Book</h2>
                <p>This technical book is designed for AI students and developers entering humanoid robotics. Each chapter builds upon the previous to provide a comprehensive understanding of ROS 2 in the context of humanoid robotics applications.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}