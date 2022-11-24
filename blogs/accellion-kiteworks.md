---
title: Accellion Kiteworks
author: Michael Yee
published: True
---


# Accellion Kiteworks

Data security is a top priority for any organization. How do you ensure that your data is always secure, confidential, accurate, reliable, available and under your control?

In this blog, I will provide an overview of the security features and capabilities of Accellion's secure file
sharing platform.

# Let's go!

The design principle behind Accellion’s secure file sharing platform is a military layering tactic. The platform enforces security at the application, data, transport and network layer (think OSI mode) to provide the organization time to detect and respond to an attack.

## First Line of Defense – Network Security

Network topology is the key to creating secure networks. 

Accellion offers five secure deployment options: On Premises Private Cloud, Customer Hosted IaaS, Accellion
Hosted Private Cloud, Hosted FedRAMP, and Hybrid Private Cloud.

### On-Prem Private Cloud Deployment

This type of deployment is done on your premises, using a VMware or Hyper-V virtual machine. On-prem environments offer the highest levels of security and control as they enable the enterprise to keep servers, storage, application service, meta-data, and
authentication within the organization’s firewall. Most security-conscious organizations tend to prefer an on-prem deployment.

On-prem deployments that are 100% on premises create a private cloud environment in the company’s data center for a single-tenant dedicated instance that prevents any co-mingling of data. Furthermore, the organization itself controls the encryption keys;
Accellion does not have any access to customer data.

### Customer Hosted IaaS Deployment

Customers who want to deploy Accellion on their AWS or Azure resources can deploy it in the same way they would on their VMware or Hyper-V systems on premises.

### Accellion Hosted Private Cloud Deployment

This type of deployment is hosted by Accellion, using Microsoft AWS or Azure.

Hosted deployments enable enterprises to rapidly implement secure file sharing, quickly scale resources and teams, and manage peaks in usage.

The hosted private cloud deployment provides a dedicated instance with no co-mingling of data. It gives the customer full control of application policies and system settings.

### Hosted FedRAMP Deployment

Accellion’s FedRAMP authorized solution for moderate impact data is available to Government agencies and commercial businesses in isolated environments on AWS.

This deployment option is ideal for organizations that require the highest level of security or are required by the Federal Government to have a compliant security plan for sharing data. Compliance with ITAR is one such example.

FedRAMP authorization requires an extensive application process involving thorough documentation of Accellion’s security processes, assessments of related systems, creation of a System Security Plan, and training and certification of Accellion employees who have access to the FedRAMP environment – over 400 controls in total.

Accellion has assembled a team of security and IT experts to support FedRAMP customers and, per FedRAMP requirements, this team is comprised of US citizens, based within the United States.

In order to retain FedRAMP Authorization status, Accellion undergoes continuous monitoring, vulnerability scanning, and annual audits of our controls. These audits are performed by a Third Party Assessment Organization (3PAO), which is also
FedRAMP authorized.

## Hybrid Deployment

Accellion also offers an on-prem and hosted hybrid private cloud deployment. Hybrid deployments are ideal for capacity planning and for supporting remote access.

The hybrid deployment mixes on-prem servers and hosted servers for selected roles (such as storage) and Enterprise Connect applications (such as SharePoint), separated by firewall from the hosted private cloud deployment that delivers a single tenant environment.

## Second Line of Defense – Application Security

Accellion provides an extensive suite of account access and authentication policy management features that can be customized to meet your business requirements. Many of the features are configurable by your IT Administrators. Your enterprise can determine
the level of control that needs to be exercised for corporate file access and tracking. Account Access and Authentication
Accellion provides comprehensive and flexible sign-in and authentication management tools.

### Sign in

Accellion uses OAuth authentication for user sign-in to the server. Users are required to enter their user name and password. Upon successful authentication, the application retrieves an access token from the server that is used in further communications with the server during the session.

### Authentication

Accellion provides configurable authentication policies for password, files, data,
and URL calls.

### Single Sign-on and LDAP integration

For Enterprise accounts, Accellion provides your IT Administrators with the ability to
centralize user account control and management using the following features:

- Active Directory/multi-LDAP/LDAPS
- SAML 2.0 and Kerberos integration to support single sign-on and information exchange between different security domains.

### Two-Factor Authentication

For enterprises that use 2FA, Accellion leverages the industry standard RADIUS protocol to
integrate with the customer’s 2FA solution.

2FA for Accellion can be integrated with any server using the RADIUS protocol. Accellion passes the user’s authentication credentials over RADIUS protocol to the 2FA RADIUS server. The server’s response determines if the user can sign in or not.

Accellion guides customers in choosing the authentication flow that is appropriate and required for their 2FA solution. Accellion has a one-time password option that administrators can enable for occasions when external users don’t have access to an enterprise’s internal RADIUS system.

### Pre-Authentication Redirect Login Flow
Accellion enables IT Administrators to implement an alternative login flow for users of singlesign on (SSO) services, including SSO services that work with Personal Identity Verification (PIV) and Common Access Card (CAC) cards, which are mandated by several U.S. government agencies. When this alternative login flow is enabled, Accellion prompts users
for a username or email address before displaying a password field. Once the username or email address is entered, Accellion takes one of two actions. If the user is registered with an SSO service, Accellion automatically redirects the user to the organization’s SSO identity provider, so the user can enter his/her password for the SSO service. If the user is not an
SSO user, Accellion displays the standard password field for the user’s Accellion account.

### Password History Policy

IT Administrators can set a policy to allow or disallow the re-use of passwords by users.

## Anti-Virus

Anti-virus software is integrated within kiteworks to scan files being uploaded to any Enterprise Content Management (ECM) system connected to Accellion or to Accellion itself. If a file containing a virus is found, kiteworks immediately quarantines the file and prevents it from being uploaded. The anti-virus service can be enabled or disabled by IT Administrators. Accellion uses F-secure anti-virus software for multi-device Internet security for PC, Mac, smartphone, and tablet.

### Advanced Threat Prevention, including Zero-Day Attacks

Leveraging integrations with leading Advanced Threat Prevention (ATP) solutions, Accellion provides organizations an integrated governance framework over all of the content entering or leaving the organization to prevent malware from infiltrating the organization’s network. Granular visibility and control of content going through the Accellion platform enables
organizations to analyze and either block or simply report on any threats of malicious data detected by the ATP solution.

### Data Loss Prevention

IT Administrators can integrate Accellion with popular Data Loss Prevention (DLP) systems that support the Internet Content Adaptation Protocol (ICAP) such as Forcepoint, Trend Micro, Symantec, Fidelis, Palisade Systems, and Digital Guardian.
Once integrated, Accellion can be configured to run a DLP scan on any file downloaded from a connected ECM system or uploaded to a cloud based content system to ensure that no data privacy policies are being violated. If a file violates the DLP policies, it is marked as non-compliant and put into quarantine to prevent it from being downloaded, uploaded or shared. Both the sender and recipient are notified of the quarantine. Only IT Administrators can remove a file from quarantine. By supporting DLP scans, Accellion helps prevent Personally Identifiable Information (PII) and other sensitive data from being inadvertently
leaked.

### Folder Permissions

Accellion provides robust yet flexible folder permission management features to enable your IT Administrators to control access to enterprise content across the organization.

The following folder permissions management features are available:

- File Tracking: Folder Owners, Managers, and Collaborators can view activity logs to see who has accessed a folder, and downloaded/uploaded/edited/deleted files, and added comments.
- Notifications: Folder Owners, Managers, Collaborators, and Downloaders can subscribe to receive e-mail alerts when files or comments are added by members, i.e. anyone with access to a folder.
- Secure Links: Folder Owners, Managers, and Collaborators can share files securely by sending recipients a secure link to their files.
- Collaboration: Folder Owners and Managers can manage users and internal and external stakeholders who have access permissions to their secure folders by assigning them user roles depending on business requirements.
- Online Viewer: Viewers can view documents within the browser or Mobile App without being granted permission to download them. This feature increases not only user productivity but also data security since it does not store local copies of documents
on endpoints. 

### Desktop File Synchronization

Accellion provides robust, secure, and flexible file synchronization. Your IT Administrators can enable continuous sync, on-demand sync, or scheduled sync. Once folder sync has been enabled, users with Manager privileges can enable or disable sync for individual folders.

Accellion file synchronization security features include:

- Authenticating kiteworks desktop client sessions through OAuth.
- Authenticating end-users to the kiteworks desktop client through LDAP/AD, SAML, and Kerberos.
- Enabling IT Administrators to view kiteworks activity logs and track files that are being synchronized.
- Set the desktop clients to encrypt the synced data and lock the sync folder when not in use.
- Remote wipe for desktop clients.

## Mobile Push and Mobile Sync

Data is protected with encrypted containers that can be remotely wiped by an IT Administrator should a mobile device be lost or stolen or the device owner leaves the organization.

## Audit Trail

Accellion automatically logs all file and user activities in the application. The audit log provides your IT Administrators full insight into system activities, user activities, file activities, and overall system health. Audit trails and comprehensive file tracking help enterprise organizations demonstrate compliance with internal policies and government regulations. Audit logs are date/time stamped and tracked by user, email address, IP address, and action taken. IT Administrators can sort by these attributes and also export the audit log either as a CSV file or to a Syslog server. Finally, your IT Administrator
determines how long logs are stored on the platform. 

Other applicaiton security features:

- Advanced Governance and eDiscovery
- FIPS 140-2
- Geographical Segregation and Data Sovereignty
- Industry and government regulations compliances

## Third Line of Defense – Data Security

Accellion offers an extremely secure data encryption strategy.

### Encryption

Accellion encrypts all content in its system, whether the files are in transit or at rest. Data in transit is secured via an SSL/TLS encrypted connection. Data at rest is encrypted with 256-bit AES encryption. 

### User-friendly Digital Rights Management (DRM)

Integrated user-friendly DRM capabilities enhance the protection of documents without sacrificing end-user productivity. DRM features include a View Only role, custom watermarking, and the ability to withdraw files.

- View Only Role - Users can only view content within the browser or Mobile App, and cannot download or synchronize content to their desktop or device.
- Watermarking - Users can only view an image of the file with a customizable watermark. Watermarks deter unauthorized file sharing via screen capture or hard copy printing.
- File Withdraw - Users can withdraw previously sent files. Once withdrawn, file links immediately expire, preventing recipients from accessing content.

### Secure Message Transmission with or without Email Attachments

When sending email messages, web and Outlook users of Accellion have the option of securing the attachment alone, the message body alone, or both. IT Administrators have the option of requiring all message bodies to be secured.

## Fourth Line of Defense – Secure Processes

### Updates

Accellion provides periodic updates to keep system libraries up-to-date.

### Security Processes

Several security processes are followed to ensure major risks are accounted.

### Security Updates

Regular security updates are made to mitigate and resolve vulnerabilities. Policy enforcement updates are performed. Kernel and software updates are made to avoid security risks.

### Patch Management

Accellion rolls out patches on a priority basis. Because the Accellion appliance includes the operating system, database server, webserver, and the application, Accellion’s patches cover all of these pieces. IT Administrators don’t have to monitor each piece for patch updates or worry about compatibility. The sever monitors for patches and, when a patch is available, IT Administrators apply the patch with one click. 

### Security-Audits

Accellion products undergo regular 3rd party security audits.

## Mobile Security

- File encryption
- PIN and Touch ID
- Mobile Data Encryption
- SSL/TLS Network Communication
- Secure Authentication

## Security Features Under Administrator Control

- Access to Enterprise Connectors (i.e. SharePoint or Windows File Share)
- Application Whitelisting
- Domain Whitelisting
- Configurable Terms of Service
- Custom LDAP/AD Mapping
- Enforced Security of Email Message Bodies
- Hash “Fingerprint” on Sent Files
- IP Restrictions for Enterprise Content Sources
- MDM Integration
- Remote Wipe of Mobile Devices
- Request File Controls per User Profile
- User Role Restrictions

## Security Features Under End-user Control

### Access Control Lists

When emailing files from Accellion, end users can control who can download the file via the secure link, how long the secure link will work, and how many downloads the secure link will allow.

### Authentication

When emailing files from Accellion, end-users can apply security settings to specify whether the recipient must authenticate his/her identity before downloading the file. While authentication is necessary to capture the audit trail, some use cases do not require users to take this additional step.

### Documents
End-users can control who can upload, download, view, print, edit, or send documents. They can also withdraw a document previously sent by kiteworks email. End-users can also set a document’s expiration date.

### Secure Email Body

End users can secure the email body in addition to the attachments. Recipients will get a secure link to access the email body, which directs them to authenticate with kiteworks to access the message content. 

### Watermarks
When an end user emails a file, Accellion places by default a custom watermark in the file that is unique to the file recipient. The sender can choose to add additional information to the watermark. (Watermarks may have custom content specified by the Accellion Administrator as well.)

# Conclusion

If your organization requires full visibility and control of your most sensitive data as it is shared securely externally, Accellion Kiteworks might be the platform for you.

The three key benefits of Acellion’s architecture are:

- reduced attack surface
- data integrity
- high scalability and availability
