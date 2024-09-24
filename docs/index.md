---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "GroundStation"
  text: "Rocket Monitoring Reimagined 🚀"
  tagline: Developed by Nathan Samuell for AIAA-UH
  actions:
    - theme: brand
      text: Get Started
      link: /markdown-examples
    - theme: alt
      text: API Examples
      link: /api-examples
    - theme: alt
      text: GitHub
      link: https://github.com/nathansamuell/groundStation

features:
  - title: Real-Time monitoring
    details: View formatted and processed data in real-time from your rocket
  - title: Visuals
    details: IN PROGRESS
  - title: No file corruptions
    details: Flight data is saved to backup files to prevent data loss in the event of power loss or app failure
  - title: APRS Broadcasting
    details: Share your rocket's status with spectators around the world
---
  
  


<script setup>
import { VPTeamMembers } from 'vitepress/theme'

const members = [
  {
    avatar: 'https://www.github.com/nathansamuell.png',
    name: 'Nathan Samuell',
    title: 'Creator',
    links: [
      { icon: 'github', link: 'https://github.com/yyx990803' },
      { icon: 'linkedin', link: 'https://linkedin.com/in/nathan-samuell' }
    ]
  },
]
</script>
  


  
# Our Team

Say hello to our awesome team.

<VPTeamMembers size="small" :members="members" />