package com.Project.InventoryManagement;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.Project.InventoryManagement.Service.InventoryService;

@SpringBootApplication
public class InventoryManagementApplication implements CommandLineRunner{
	public static void main(String[] args) {
		SpringApplication.run(InventoryManagementApplication.class, args);
	}

	@Override
    public void run(String... args) throws Exception {
        System.out.println("Application started.");
    }


}
