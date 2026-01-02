# Ampere Computing & ARM64 Architecture Explained

## Overview

**Ampere Computing** is the ARM-based CPU manufacturer that Oracle uses for its Always-Free tier instances (VM.Standard.A1.Flex).

## Key Facts

- **Founded:** 2017 by former Intel executives
- **Ownership:** Oracle has substantial stake in Ampere (2021)
- **Architecture:** ARM64 (RISC-based)
- **Why Oracle Uses It:** Cost-effective, power-efficient, high performance

## Your Always-Free Instance Specs

```
Shape: VM.Standard.A1.Flex
CPU:   4 OCPU @ Ampere Altra ARM64
Memory: 24 GB RAM
Storage: Up to 200GB total
Cost:  $0.00/month (verified)
```

## ARM64 vs x86 (Intel/AMD)

| Feature | ARM64 (Ampere) | x86 (Intel/AMD) |
|---------|----------------|-----------------|
| **Power** | Very Low | Higher |
| **Performance** | Excellent for cloud | Good for general |
| **Compatibility** | Linux ARM64 apps only | Most software |
| **Best Use** | Docker, web servers, cloud | Desktop, legacy |

## What Works on ARM64

### ✅ Excellent Support:
- **Docker containers** (use multi-arch images)
- **All major Linux distributions** (Ubuntu, Debian, etc.)
- **Web servers** (Nginx, Apache)
- **Databases** (PostgreSQL, MySQL, Redis, MongoDB)
- **Programming languages** (Python, Node.js, Go, Rust)
- **Development tools** (Git, Docker, VS Code Server)
- **Personal cloud apps** (Nextcloud, Jellyfin)
- **VPN servers** (WireGuard, OpenVPN)

### ⚠️ May Need ARM64 Version:
- Some proprietary software
- Old/legacy applications
- Windows software (won't work)

## Docker on ARM64

```bash
# Multi-arch images automatically use ARM64
docker run -d nginx:latest

# Or specify explicitly
docker run -d --platform linux/arm64 nginx:latest

# Build for ARM64
docker build --platform linux/arm64 -t myapp .
```

Docker Compose example:
```yaml
web:
  image: nginx:latest
  platform: linux/arm64
  ports:
    - "80:80"
```

## Why This is a Great Deal

**4 OCPU + 24GB RAM for $0.00/month is exceptional because:**

1. **Oracle owns Ampere** - lower CPU costs for them
2. **Power efficient** - cheaper to operate
3. **Cloud-optimized** - ARM64 designed for modern workloads
4. **Economically sustainable** - Oracle can afford to give it free

## Performance

For most cloud workloads (web servers, Docker, databases), ARM64 performance is **comparable to x86**. The 4 OCPU handles:
- Multiple Docker containers
- Development environments
- Personal web applications
- Media streaming (with ARM64 builds)
- Database servers
- VPN endpoints

## Summary

Your Always-Free instance uses:
- **Ampere Altra ARM64 processor** (modern, efficient)
- **4 cores @ ~3GHz** (excellent performance)
- **24GB DDR4 RAM** (generous allocation)
- **$0.00/month cost** (verified Always-Free)

**It's a modern, powerful, and completely free platform for self-hosting!**

For complete setup instructions, see [ALWAYS_FREE_SETUP.md](./ALWAYS_FREE_SETUP.md)