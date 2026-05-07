-- TourDB Database Schema for SQL Server
USE TourDB;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Phone VARCHAR(15) NULL,
    Address NVARCHAR(255) NULL,
    Role VARCHAR(20) DEFAULT 'Customer',
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Categories')
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL
);
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Tours')
CREATE TABLE Tours (
    TourID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryID INT FOREIGN KEY REFERENCES Categories(CategoryID),
    TourName NVARCHAR(255) NOT NULL,
    Description NTEXT NULL,
    Price FLOAT NULL,
    Duration VARCHAR(50) NULL,
    DepartureLocation NVARCHAR(100) NULL,
    ImageThumbnail VARCHAR(255) NULL,
    ImageUrl VARCHAR(255) NULL
);
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Bookings')
CREATE TABLE Bookings (
    BookingID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID) NOT NULL,
    TourID INT FOREIGN KEY REFERENCES Tours(TourID) NOT NULL,
    BookingDate DATETIME DEFAULT GETDATE(),
    TravelDate DATETIME NOT NULL,
    NumberOfPeople INT DEFAULT 1 NOT NULL,
    TotalPrice FLOAT NULL,
    Status NVARCHAR(50) DEFAULT N'Đang chờ duyệt',
    PaymentMethod NVARCHAR(50) NULL,
    Note NVARCHAR(500) NULL
);
GO
