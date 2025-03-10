package com.Project.InventoryManagement;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.Project.InventoryManagement.Service.InventoryService;

@SpringBootApplication
public class InventoryManagementApplication implements CommandLineRunner{
	private final InventoryService inventoryService;

	@Autowired
	public InventoryManagementApplication(InventoryService inventoryService){
		this.inventoryService = inventoryService;
	}

	public static void main(String[] args) {
		SpringApplication.run(InventoryManagementApplication.class, args);
	}

	@Override
	public void run(String... args){
		int i = 0;
	}
	// resst controller with jwt authentication and react api

}
