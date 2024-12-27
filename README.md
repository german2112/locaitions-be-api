## **Overview**
This project is a robust Python-based API built using **FastAPI**, designed to power a mobile application developed in **Flutter**. The application’s primary objective is to provide users with live ratings for nearby locations based on user-generated reviews. The API leverages various cutting-edge technologies, including MongoDB, Kafka, AWS services, and Google Maps API, to deliver fast, reliable, and scalable functionality.

Due to the size and complexity of the project, a **monolithic architecture** was chosen, ensuring streamlined development and simplified management. The monolithic structure effectively accommodates the requirements of a tightly integrated mobile application.

---

## **Features**
1. **Location-Based Ratings**:  
   - Retrieves live ratings for locations using Google Maps API to find nearby points of interest based on user location.

2. **User Reviews Management**:  
   - Accepts and processes user reviews to calculate dynamic ratings for locations.

3. **Real-Time Data Processing**:  
   - Utilizes **Kafka** for efficient real-time data processing of user reviews and ratings updates.

4. **Image Recognition**:  
   - Integrates **AWS Rekognition** to analyze user-uploaded images for content validation and to associate images with locations.

5. **Cloud Storage**:  
   - Stores user-generated media such as images and videos on **AWS S3** for high availability and scalability.

6. **Database**:  
   - Employs **MongoDB** for managing dynamic, unstructured data related to locations, reviews, and ratings.
   - Utilizes **MongoDB Realm** for serverless functions and data triggers, enabling automation of specific database operations.

7. **Deployment and Scalability**:  
   - API hosted on **AWS EC2** for high-performance computing.
   - Scalable microservices run on **AWS Fargate**, ensuring flexibility and reliability in handling traffic spikes.

---

## **Technologies Used**

### **Core Framework and Programming Language**:
- **FastAPI**: Chosen for its speed, asynchronous capabilities, and built-in support for OpenAPI documentation.
- **Python**: Provides flexibility and a vast ecosystem of libraries to support complex requirements.

### **Database**:
- **MongoDB**: Schema-less, highly scalable, and suitable for storing unstructured and hierarchical data.
- **MongoDB Realm**: Automates database triggers and offers serverless backend capabilities.

### **Message Queue**:
- **Apache Kafka**: Handles asynchronous message processing for real-time data synchronization and updates.

### **Cloud Services**:
- **AWS Rekognition**: Provides advanced image analysis for validating and associating user-uploaded images with locations.
- **AWS S3**: Ensures reliable storage for media files with low-latency access.
- **AWS EC2**: Offers robust hosting for the monolithic API, ensuring high performance.
- **AWS Fargate**: Runs containerized services for task-based microservices, providing scalability and reduced operational overhead.

### **Geospatial Data**:
- **Google Maps API**: Facilitates location-based searches and retrieves nearby points of interest.

---

## **Requirements**

### **Prerequisites**:
- **Python 3.9+**: Ensure you have Python installed on your system.
- **MongoDB**: Use MongoDB Atlas or a local instance for database management.
- **Kafka Cluster**: Set up or connect to an existing Kafka cluster for message queuing.
- **AWS Credentials**: Ensure you have IAM roles with the necessary permissions for:
  - **AWS Rekognition**
  - **AWS S3**
  - **AWS EC2**
  - **AWS Fargate**



### **Scalability and Future Enhancements**:
While the current monolithic architecture suits the project scope, future iterations could consider transitioning to a microservices architecture to further enhance scalability and maintainability.

### **Potential Enhancements**:
Implement GraphQL to optimize API queries.
Add real-time WebSocket updates for dynamic rating changes.
Integrate a machine learning model for predicting location popularity trends.

### **Conclusion**
The Live Ratings API is a high-performance, feature-rich backend solution designed to power location-based, real-time applications. By leveraging modern frameworks and cloud services, it offers scalability, reliability, and ease of integration with client-side applications.


